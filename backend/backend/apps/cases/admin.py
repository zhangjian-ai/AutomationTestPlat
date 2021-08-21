from django.contrib import admin

from .models import *


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'uuid', 'name', 'parent', 'creator']

    # 过滤器
    list_filter = ['parent', 'creator']

    ordering = ['-id']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'no', 'name', 'module', 'priority', 'is_auto', 'author', 'creator', 'reviser', 'create_time']
    # 排序。此处为按id升序，降序：'-id'
    ordering = ['-id']
    # 收索框查找的字段。外键需要指明匹配外键对象的具体字段
    search_fields = ['no', 'name', 'module__name', 'priority', 'author', 'is_auto', 'status', 'reviser__nickname']
    # 过滤器
    list_filter = ['module__name', 'priority', 'is_auto']
    # 分页
    list_per_page = 15
