from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    """图片序列化器"""

    class Meta:
        model = Image
        fields = ['type', 'location', 'image']

        extra_kwargs = {
            'type': {
                'required': True
            },
            'location': {
                'required': True
            },
            'image': {
                'required': True,
            }
        }

    def validate(self, attrs):
        """
        传参检查
        :param attrs:
        :return:
        """
        if attrs.get('type') not in (x[0] for x in Image.IMAGE_TYPE):
            raise serializers.ValidationError('图片类型不合法')

        return attrs
