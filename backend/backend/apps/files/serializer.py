from rest_framework import serializers

from .models import *


class SystemImageSerializer(serializers.ModelSerializer):
    """系统图片序列化器"""

    scope_str = serializers.CharField(source='get_scope_display', read_only=True)

    class Meta:
        model = Image
        fields = '__all__'


class SystemFileSerializer(serializers.ModelSerializer):
    """系统静态文件序列化器"""

    scope_str = serializers.CharField(source='get_scope_display', read_only=True)

    class Meta:
        model = File
        fields = '__all__'


class SourceListSerializer(serializers.ModelSerializer):
    """资源列表序列化器"""

    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = SourceModel
        fields = '__all__'
