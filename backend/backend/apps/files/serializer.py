from rest_framework import serializers

from .models import Image


class SystemImageSerializer(serializers.ModelSerializer):
    """系统图片序列化器"""

    class Meta:
        model = Image
        fields = '__all__'
