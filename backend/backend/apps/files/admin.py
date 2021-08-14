from django.contrib import admin

from .models import *


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'name', 'scope', 'image', 'create_time']
