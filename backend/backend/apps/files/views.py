import re
import traceback
import logging

from fdfs_client.exceptions import DataError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Image
from .serializer import SystemImageSerializer
from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage


logger = logging.getLogger('test_plat')


class SystemImageView(APIView):
    """图片链接视图"""

    permission_classes = []

    def get(self, request, scope):
        # 映射关系
        map_scope = {
            'login': 0,
            'home': 1,
            'case': 2,
            'job': 3
        }

        # 查询集
        try:
            querySet = Image.objects.filter(scope=map_scope[scope])
        except Image.DoesNotExist:
            logger.warning(f'图片信息不存在，scope: {scope}')
            return Response({'msg': '图片信息不存在'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SystemImageSerializer(instance=querySet, many=True)
        image = dict()
        for data in serializer.data:
            image[data['name']] = data['image']

        return Response(image)


class ImageView(APIView):
    """图片视图"""

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
