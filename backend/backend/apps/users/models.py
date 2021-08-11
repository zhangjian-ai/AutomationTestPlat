from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    用户模型类。自定义用户模型类之后，要在配置文件中指明，否则仍然默认django自己的模型类
    继承django本身的用户模型类，增加一个mobile字段
    django本身的用户模型类，包含 set_password、check_password两个方法来加密和校验密码
    """

    nickname = models.CharField(max_length=20, default='', verbose_name='昵称')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'tp_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname
