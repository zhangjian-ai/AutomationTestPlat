import re

from django_redis import get_redis_connection
from rest_framework import serializers

from .models import User
from backend.utils.helper import create_jwt_token


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """

    password2 = serializers.CharField(label='确认密码', write_only=True)
    smsCode = serializers.CharField(label='短信验证码', write_only=True)
    nickname = serializers.CharField(label='昵称')

    # 再新增一个token字段，用于返回给前端
    token = serializers.CharField(label='TOKEN', read_only=True, default=None)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'smsCode', 'nickname', 'token', 'email']

        # 修改指定参数的校验规则
        extra_kwargs = {
            'username': {
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户名长度不能小于6位',
                    'max_length': '用户名长度不能大于20位'
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户名长度不能小于8位',
                    'max_length': '用户名长度不能大于20位'
                }
            },
            'mobile': {
                'write_only': True
            },
            'email': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        """
        验证数据
        :param attrs:
        :return:
        """
        # 验证手机号
        mobile = attrs.get('mobile')

        if not re.match(r"^1[3-9]\d{9}$", mobile):
            raise serializers.ValidationError('手机号不合法。')

        # 验证两次输入的密码是否一致
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError('两次输入密码不一致。')

        # 校验短信验证码
        redis_conn = get_redis_connection('default')
        real_sms_code = redis_conn.get('sms_%s' % mobile).decode()

        if real_sms_code is None or attrs.get('smsCode') != real_sms_code:
            raise serializers.ValidationError('短信验证码错误或已过期。')

        # 校验否通过，则返回
        return attrs

    def create(self, validated_data):
        """
        重写父类create方法
        :param validated_data:
        :return:
        """

        # 删除掉不需要写入数据库的字段
        del validated_data['password2']
        del validated_data['smsCode']

        # 取出密码
        password = validated_data.pop('password')

        # 设置账号在职状态 是否可登陆管理后台
        # validated_data['is_staff'] = 1

        # 新建用户对象
        user = User(**validated_data)

        # 调用父类的set_password方法，加密密码并保存
        user.set_password(password)
        user.save()

        # 此时还缺少序列化字段token
        token = create_jwt_token(user)

        user.token = token

        # 返回的对象将被序列化到serializer.data中。通常都将该值作为响应返回
        return user
