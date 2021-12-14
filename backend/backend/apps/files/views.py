import json
import re
import traceback
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from fdfs_client.exceptions import DataError
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializer import SystemImageSerializer, SystemFileSerializer, SourceListSerializer
from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage

logger = logging.getLogger('test_plat')


class ImageView(APIView):
    """图片视图"""

    permission_classes = []

    def get(self, request):
        querySet = Image.objects.filter()
        if querySet.count() == 0:
            logger.info("无可用的图片信息")
            return Response({'msg': '无可用的图片信息'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SystemImageSerializer(instance=querySet, many=True)
        image = dict()
        for data in serializer.data:
            image[data['scope_str']] = data['image']

        return Response(image)

    def post(self, request):
        # 获取上传文件内容
        content = request.data.get('file')

        # 保存到文件服务器
        try:
            storage = FastDFSStorage()
            file_id = storage._save(name=content.__str__(), content=content)
            url = storage.url(file_id)
        except Exception as e:
            logger.error(traceback.format_exc())
            return Response({'msg': f'图片上传失败:{e}'})
        return Response({'url': url}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        # 获取url
        url = request.data.get('url')

        storage = FastDFSStorage()
        # 正则匹配出file_id
        file_id = re.findall(rf'{storage.base_url}(.+?)$', url)[0]
        try:
            storage.delete(file_id)
        except DataError:
            logger.warning(traceback.format_exc())
            return Response({'msg': '要删除的文件不存在'})
        return Response({'msg': f'{url}:删除成功'})


class FileView(APIView):
    permission_classes = []

    def get(self, request):
        querySet = File.objects.filter()
        if querySet.count() == 0:
            logger.info("无可用的静态文件")
            return Response({'msg': '无可用的静态文件'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SystemFileSerializer(instance=querySet, many=True)
        image = dict()
        for data in serializer.data:
            image[data['scope_str']] = data['id']

        return Response(image)

    def post(self, request):
        # 获取前端传入的file_id
        temp_id = request.data.get('temp_id')

        # 根据file_id获取文件名
        try:
            query = File.objects.get(id=temp_id)
        except ObjectDoesNotExist:
            return Response({'msg': '静态资源不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 从仓库读取文件流
        dfs = FastDFSStorage()
        content = dfs.client.download_to_buffer(query.file.__str__().encode())

        # 获取二进制文件，存入响应对象
        response = HttpResponse(content['Content'], content_type='application/octet-stream')
        # 添加自定义响应头，传递文件名
        response['Content-Dispositon'] = f"attachment; filename={query.name}"
        # 暴露自定义header，这样在js中才能获取到该值
        response['Access-Control-Expose-Headers'] = 'Content-Dispositon'

        return response


class SourceListView(ListAPIView):
    """资源视图"""
    serializer_class = SourceListSerializer

    def get_queryset(self):
        # 获取请求参数，前端传入的对象，被默认转成了字符串：'{}'
        conditions = self.request.query_params.get('conditions')
        # 把字符串转换成对应的字典
        conditions = json.loads(conditions)

        # 处理掉空值，避免干扰查询
        valid_conditions = dict()
        for key, value in conditions.items():
            if value not in ("", None):
                valid_conditions[key] = value

        # 资源名称提供模糊查询
        name = valid_conditions.pop('name', "")

        # 创建时间为范围匹配
        create_time = valid_conditions.pop('create_time', None)

        if create_time:
            instances = SourceModel.objects.filter(**valid_conditions, name__contains=name,
                                                   create_time__gte=create_time[0],
                                                   create_time__lte=create_time[1]).values()
        else:
            instances = SourceModel.objects.filter(**valid_conditions, name__contains=name).values()

        # 根据uid进行分组。Django ORM 的分组很拉垮
        temp_list = []
        source_list = []

        for item in instances:
            if item['uid'] not in temp_list:
                temp_list.append(item['uid'])
                source_list.append(item)

        return source_list
