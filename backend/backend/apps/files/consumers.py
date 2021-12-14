import json
import math

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from django.db import DataError
from fdfs_client.exceptions import DataError as FdfsDataError, ConnectionError

from files.models import SourceModel
from files.serializer import SourceListSerializer
from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage
from rest_framework.exceptions import ValidationError


class SourceUploadConsumer(WebsocketConsumer):
    source_info = None
    content = b''

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
                # del self.source_info['size_byte']

                # 将文件按 25M 一份存入服务器
                count = 0
                size = 25 * 1024 * 1024
                total = math.ceil(len(self.content) / size)

                while count < total:
                    # 保存文件到服务器
                    try:
                        file_id = client._save(name=self.source_info['name'],
                                               content=self.content[count * size: (count + 1) * size])
                        self.source_info['file_id'] = file_id

                        # 保存资源信息到数据库
                        SourceModel.objects.create(**self.source_info)
                    except (ConnectionError, FdfsDataError, DataError, TypeError) as e:
                        # 文件服务器连接异常/数据库写入异常
                        self.send(rf"saving.{str(e)}")
                        self.close()
                        raise StopConsumer
                    else:
                        # 计数器累加，并返回当前进度
                        count += 1
                        self.send(rf"saving.当前写入进度: {count} / {total}")

                # 向前端发送结束标识
                self.send(text_data="close.写入完成，上传成功。")

                # 断开连接
                self.close()
                raise StopConsumer

        self.send(text_data="continue.")

    def websocket_disconnect(self, message):
        # 断开连接
        raise StopConsumer


class SourceDownloadConsumer(WebsocketConsumer):
    source_info = None
    content = b''
    count = 0
    size = 102400
    total = 0

    def websocket_connect(self, message):
        # 服务端允许客户端创建连接
        self.accept()

    def websocket_receive(self, message):
        # 判断是否是首次接收到客户端信息，如果是就根据 uid 查询资源信息
        if not self.source_info:
            uid = json.loads(message['text'])

            try:
                # 查询数据库
                query_set = SourceModel.objects.filter(uid=uid).order_by('id')
                serializer = SourceListSerializer(instance=query_set, many=True)
                self.source_info = serializer.data

                # 实例文件服务器客户端
                client = FastDFSStorage()

                # 从文件服务器拉取资源
                count = 0
                for item in self.source_info:
                    count += 1
                    self.send(rf"prepare.{count}")
                    self.content += client.client.download_to_buffer(item['file_id'].encode())['Content']

                # 计算资源的真实大小
                self.total = len(self.content)

            except (ConnectionError, FdfsDataError, DataError, TypeError, AttributeError, ValidationError) as e:
                self.send(rf"error.{str(e)}")
                self.close()
                raise StopConsumer

            # 通知客户端资源已准备好，可以开始向客户端传输
            self.send(rf"ready.{self.total}")

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
