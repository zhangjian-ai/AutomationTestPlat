import logging
import random

from django_redis import get_redis_connection
from django.conf import settings
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from DingTalkLoginTool.dingtalk import AuthDT

from users.models import User
from backend.utils.helper import create_jwt_token
from backend.utils import constants
from celery_tasks.sms.tasks import send_sms_code

from encrypt.encrypt import load_public_key

logger = logging.getLogger('test_plat')

# 实例化钉钉工具类
dt = AuthDT(appid=settings.DT_APP_ID, app_secret=settings.DT_CLIENT_SECRET,
            redirect_uri=settings.DT_REDIRECT_URI, app_key=settings.DT_APP_KEY)


class SmsCodeView(APIView):
    """
    发送短信验证码
    """

    permission_classes = []
    authentication_classes = []

    def get(self, request, mobile):
        # 连接redis
        redis_conn = get_redis_connection('default')

        # 判断短信发送周期
        send_flag = redis_conn.get('sms_flag_%s' % mobile)

        if send_flag:
            return Response({'msg': '验证短信发送过于频繁，请稍后再试'}, status=status.HTTP_403_FORBIDDEN)

        # 生成验证码
        sms_code = str(random.randint(0, 999999)).zfill(6)

        # 创建redis管道对象，缓存验证码和发送标识
        pip = redis_conn.pipeline()
        pip.setex('sms_%s' % mobile, constants.SMS_CODE_EXPIRES, sms_code)
        pip.setex('sms_flag_%s' % mobile, constants.SMS_CODE_INTERVAL, 1)
        pip.execute()

        # 调用异步任务发送短信
        send_sms_code.delay(mobile, sms_code, constants.SMS_CODE_EXPIRES, constants.SMS_TEMPLATE_ID)

        # debug阶段将code返回
        return Response({'code': sms_code, 'msg': '短信验证验证码发送成功。'})


class DingTalkAuth(APIView):
    """钉钉登陆"""

    permission_classes = []

    def get(self, request):
        """
        获取登陆URL
        :param request:
        :return:
        """
        loginTmpCode = request.query_params.get('loginTmpCode')
        url = dt.get_dt_url(loginTmpCode=loginTmpCode)

        return Response({'url': url})

    def post(self, request):
        """
        登陆账户或者新建后自动登录
        :param request:
        :return:
        """
        code = request.data.get('code')
        if not code:
            logger.error('缺少code码，登录失败。')
            return Response({'msg': '缺少code，回调失败。'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取unionid
        unionid = dt.get_unionid(code)

        # 获取access_token
        access_token = dt.get_access_token()

        # 获取userid
        userid = dt.get_userid(access_token, unionid)

        # 获取用户信息
        info = dt.get_user_detail(userid, access_token)
        logger.info(f"成功获取到钉钉用户[{info['name']}]的信息。")

        # 判断用户是否存在
        try:
            user = User.objects.get(Q(username=info['userid']) | Q(mobile=info['mobile']))
        except User.DoesNotExist:
            # 如果没有则返回用户信息进行首次注册登陆
            return Response({
                "username": info['userid'],
                "email": info.get('email'),  # 邮箱可能没有
                "nickname": info['name'],
                "mobile": info['mobile'],
                "active": info['active']
            }, status=status.HTTP_202_ACCEPTED)
        else:
            # 如果存在则直接返回登陆成功的信息
            token = create_jwt_token(user)
            logger.info(f"钉钉用户[{info['name']}]登陆成功")
            return Response({
                'token': token,
                'nickname': user.nickname
            })


class CipherView(APIView):
    """密钥视图"""

    permission_classes = []

    def get(self, request):
        # 获取公钥
        content = load_public_key()

        return Response({'key': content})
