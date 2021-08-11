import re

from fdfs_client.exceptions import DataError
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ImageSerializer
from .models import Image
from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage


class UploadImageView(CreateAPIView):
    """图片上传视图"""

    serializer_class = ImageSerializer


class SystemImageUrlView(APIView):
    """图片链接视图"""

    permission_classes = []

    def get(self, request):
        # 提取参数
        location = request.query_params.get('location')

        # 查询集
        try:
            query = Image.objects.get(location=location)
        except Image.DoesNotExist:
            return Response({'msg': '图片信息不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ImageSerializer(query)

            return Response(serializer.data)


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
            return Response({'msg': '要删除的文件不存在'})
        return Response({'msg': f'{url}:删除成功'})
