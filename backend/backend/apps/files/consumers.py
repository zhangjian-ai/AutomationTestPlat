import json
import logging
import math
import threading

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from django.db import transaction, DataError
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError
from fdfs_client.exceptions import DataError as FdfsDataError, ConnectionError

from files.models import SourceModel, SourceStorePathModel
from files.serializer import SourceStorePathSerializer
from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage

from backend.utils.customSignal import plus_one

logger = logging.getLogger('test_plat')


class SourceUploadConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.source_info = None
        self.content = b''

        self.count = 0
        self.parts = 0
        # 将文件按 25M 一份存入服务器
        self.size = 25 * 1024 * 1024

        self.file_ids = []
        self.threads = []

    def write(self, client, count):
        try:
            file_id = client._save(name=self.source_info['name'],
                                   content=self.content[self.count * self.size: (self.count + 1) * self.size])
            self.file_ids.append((count, file_id))
        except (ConnectionError, FdfsDataError, DataError, TypeError) as e:
            # 文件服务器连接异常/数据库写入异常
            self.send(rf"saving.{str(e)}")
            self.close()
            raise StopConsumer

    def websocket_connect(self, message):
        # 服务端允许客户端创建连接
        self.accept()

    def websocket_receive(self, message):
        # 判断是否是首次接收到客户端信息，如果是就保存为资源信息
        if not self.source_info:
            self.source_info = json.loads(message['text'])

        # 否则追加到content
        else:
            self.content += message['bytes']

            # 上传完成之后再保存到文件服务器
            if len(self.content) == self.source_info['size_bytes']:
                # 文件接收完成，保存到文件服务器
                client = FastDFSStorage()

                # 删除不需要的字段。2021-12-13 决定保留，以作后用
                # del self.source_info['size_bytes']

                # 总共拆分成多少份
                self.parts = math.ceil(len(self.content) / self.size)

                while self.count < self.parts:
                    # 保存文件到服务器
                    t = threading.Thread(target=self.write, args=(client, self.count))
                    t.start()
                    self.threads.append(t)

                    # 计数器累加，并返回当前进度
                    self.count += 1

                for t in self.threads:
                    t.join()

                # 保存资源信息到数据库
                self.file_ids.sort(key=lambda x: x[0])

                with transaction.atomic():
                    save_id = transaction.savepoint()
                    try:
                        # 新增主表信息
                        source = SourceModel.objects.create(**self.source_info)

                        # 新增从表
                        for item in self.file_ids:
                            SourceStorePathModel.objects.create(file_id=item[1], source_id=source)
                            self.send(rf"saving.当前写入进度: {item[0] + 1} / {self.parts}")
                    except (ValueError, TypeError) as e:
                        # 如果写库失败，回滚写库操作，并删除文件服务器中的文件
                        transaction.savepoint_rollback(save_id)
                        [client.delete(item[1]) for item in self.file_ids]

                        # 向前端发送结束标识
                        self.send(text_data=f"close.{str(e)}")

                    self.send(text_data="close.写入完成，上传成功。")

                # 断开连接
                self.close()
                raise StopConsumer

        self.send(text_data="continue.")

    def websocket_disconnect(self, message):
        # 断开连接
        raise StopConsumer


class SourceDownloadConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.links = None
        self.content = b''
        self.contents = []
        self.count = 0
        self.size = 102400
        self.total = 0

        self.threads = []

    def read(self, client, count, file_id):
        # 多线程读取文件服务器资源
        try:
            content = client.client.download_to_buffer(file_id.encode())['Content']
            self.contents.append((count, content))
        except (ConnectionError, FdfsDataError) as e:
            self.send(rf"error.{str(e)}")
            self.close()
            raise StopConsumer

    def websocket_connect(self, message):
        # 服务端允许客户端创建连接
        self.accept()

    def websocket_receive(self, message):
        # 判断是否是首次接收到客户端信息，如果是就根据 uid 查询资源信息
        if not self.links:
            uid = json.loads(message['text'])

            try:
                # 查询数据库
                source = SourceModel.objects.get(uid=uid)
                serializer = SourceStorePathSerializer(instance=source.links, many=True)
                self.links = serializer.data

                # 实例文件服务器客户端
                client = FastDFSStorage()

                # 从文件服务器拉取资源
                self.send(rf"prepare.Please waiting")
                for index, item in enumerate(self.links):
                    t = threading.Thread(target=self.read, args=(client, index, item['file_id']))
                    t.start()
                    self.threads.append(t)

                for t in self.threads:
                    t.join()

                # 拼接bytes
                self.contents.sort(key=lambda x: x[0])
                for item in self.contents:
                    self.content += item[1]

                # 计算资源的真实大小
                self.total = len(self.content)

            except (DataError, TypeError, AttributeError, ValidationError) as e:
                self.send(rf"error.{str(e)}")
                self.close()
                raise StopConsumer

            # 通知客户端资源已准备好，可以开始向客户端传输
            self.send(rf"ready.{self.total}")

            # 发送下载计数+1信号
            plus_one.send(SourceDownloadConsumer, flag=True, id=source.id)

        else:
            # 判断客户端标识是否是 receiving 且 资源尚未传输完成，就继续发送资源
            if message['text'] == "receiving" and self.count * self.size < self.total:
                self.send(bytes_data=self.content[self.count * self.size: (self.count + 1) * self.size])
                self.count += 1

            # 客户端标识是 complete 表示传输完成
            if message['text'] == "complete":
                self.send("close.")
                self.close()

    def websocket_disconnect(self, message):
        # 断开连接
        raise StopConsumer


@receiver(plus_one, sender=SourceDownloadConsumer)
def download_count(sender, **kwargs):
    # 获取信号中传递的参数
    primary_id = kwargs['id']
    flag = kwargs['flag']

    # 改库
    try:
        source = SourceModel.objects.get(id=primary_id)
    except SourceModel.DoesNotExist:
        logger.error("资源下载计数累加失败[资源id不存在]")
    else:
        if flag:
            source.count += 1
            source.save()
