from django.contrib import admin

from .models import *
from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'type', 'location', 'image', 'create_time']
