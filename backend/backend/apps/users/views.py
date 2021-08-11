import logging

from django.db.models import Q
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserRegisterSerializer
from backend.utils.helper import create_jwt_token
from backend.utils import constants

logger = logging.getLogger('test_plat')


class UserRegisterView(CreateAPIView):
    """
    用户注册
    直接继承CreateAPIView，父类已经提供了post方法
    """
    # 指定序列化器
    serializer_class = UserRegisterSerializer


class CheckUserCount(APIView):
    """
    检查用户是否存在
    """

    def get(self, request):
        # 获取前端传参
        param = request.query_params.get('param')

        # 查询用户
        querySet = User.objects.filter(Q(username=param) | Q(mobile=param))
        count = len(querySet)

        return Response({'count': count})


class UserListView(ListAPIView):
    """用户列表视图"""

    permission_classes = [IsAuthenticated]

    serializer_class = UserRegisterSerializer

    def get_queryset(self):
        nickname = self.request.query_params.get("param")
        if nickname:
            querySet = User.objects.filter(nickname__icontains=nickname, is_active=True)
        else:
            querySet = User.objects.filter(is_active=True)

        return querySet


class UserLoginView(APIView):
    """登陆视图"""

    def post(self, request):
        # 获取前端数据
        data = request.data

        login_type = data.pop("type")

        # 根据登陆方式不同走不同的逻辑
        if login_type == "account":
            username = data.pop("username")
            password = data.pop("password")

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'msg': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if user.check_password(password):
                    # 密码校验成功则返回登陆信息
                    token = create_jwt_token(user)
                    logger.info(f"用户[{user.nickname}]登陆成功")
                    return Response({'nickname': user.nickname, 'token': token})
                # 密码校验失败
                return Response({'msg': '账号或密码错误'}, status=status.HTTP_400_BAD_REQUEST)

        if login_type == "mobile":
            mobile = data.pop("mobile")
            smsCode = data.pop("smsCode")

            try:
                user = User.objects.get(mobile=mobile)
            except User.DoesNotExist:
                return Response({'msg': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # 获取缓存的验证码
                redis_conn = get_redis_connection('default')
                real_smsCode = redis_conn.get('sms_%s' % mobile)
                if real_smsCode and real_smsCode.decode() == smsCode:
                    token = create_jwt_token(user)
                    logger.info(f"用户[{user.nickname}]登陆成功")
                    return Response({'nickname': user.nickname, 'token': token})
                # 密码校验失败
                return Response({'msg': '验证码错误或失效'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'msg': '不被允许的登陆方式'}, status=status.HTTP_400_BAD_REQUEST)


class GetConstantsAttrsView(APIView):
    """获取常量配置"""
    permission_classes = [IsAuthenticated]

    def get(self, request, name):
        # 获取相关属性
        if hasattr(constants, name):
            value = getattr(constants, name)
            return Response(value)
        else:
            return Response({'msg': '期望获取的值不存在'}, status=status.HTTP_400_BAD_REQUEST)
