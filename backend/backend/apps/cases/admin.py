from django.contrib import admin

from .models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'name', 'create_user', 'create_time']

    ordering = ['id']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'name', 'client', 'create_user', 'create_time']

    ordering = ['id']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'case_id', 'case_name', 'client', 'module', 'level', 'owner', 'is_auto', 'updater',
                    'create_time']
    # 排序。此处为按id升序，降序：'-id'
    ordering = ['id']
    # 收索框查找的字段。外键需要指明匹配外键对象的具体字段
    search_fields = ['case_id', 'case_name', 'client__name', 'module__name', 'level', 'owner', 'is_auto',
                     'uploader__nickname']
    # 过滤器
    list_filter = ['client', 'module', 'level', 'owner', 'is_auto', 'updater']
