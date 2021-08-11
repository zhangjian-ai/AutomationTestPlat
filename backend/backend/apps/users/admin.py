from django.contrib import admin

from .models import *

# 直接注册
admin.site.register(User)

# 修改网站标题
admin.site.site_title = "自动化测试平台 后台管理系统"
admin.site.site_header = "自动化测试平台"
