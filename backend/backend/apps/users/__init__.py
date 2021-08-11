import os

from django.apps import AppConfig

# 修改App在后台展示的名称
default_app_config = 'users.UsersConfig'


# 获取当前App的命名
def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


# 重写类FilesConfig
class UsersConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = "成员管理"
