from django.contrib import admin

from .models import *


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'scope', 'image', 'create_time']


@admin.register(File)
class ImageAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'name', 'scope', 'file', 'create_time']


@admin.register(SourceModel)
class SourceAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['uid', 'name', 'os', 'version', 'provider', 'count']
