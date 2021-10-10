import re
import traceback
import logging

from fdfs_client.exceptions import DataError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializer import SystemImageSerializer, SystemFileSerializer
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
            image[data['scope_str']] = data['file']

        return Response(image)
