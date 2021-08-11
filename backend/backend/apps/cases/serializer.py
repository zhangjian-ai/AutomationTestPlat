from rest_framework import serializers

from .models import Case, Client, Module
from backend.utils.helper import get_uuid


class CaseSerializer(serializers.ModelSerializer):
    """用例序列化器"""

    client = serializers.StringRelatedField(label="应用名称", read_only=True)
    module = serializers.StringRelatedField(label="功能模块", read_only=True)
    updater = serializers.StringRelatedField(label="更新人", read_only=True)

    client_id = serializers.IntegerField(label="应用ID", required=True)
    module_id = serializers.IntegerField(label="模块ID", required=True)

    # chioce字段 get_<字段名>_display 显示名称
    level_value = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = Case
        fields = '__all__'

    def validate(self, attrs):
        # 自动化用例exec_path不能为空
        if attrs.get('is_auto'):
            if not attrs.get('exec_path'):
                return serializers.ValidationError('is_auto为true时，exec_path必填')

        # 添加uploader
        attrs['updater'] = self.context

        return attrs


class ClientSerializer(serializers.ModelSerializer):
    """应用序列化器"""

    class Meta:
        model = Client
        fields = ['id', 'name']

    def create(self, validated_data):
        validated_data['create_user'] = self.context
        validated_data['uuid'] = get_uuid()
        Client.objects.create(**validated_data)

        return validated_data


class ModuleSerializer(serializers.ModelSerializer):
    """功能模块序列化器"""

    class Meta:
        model = Module
        fields = ['id', 'name', 'client']

    def create(self, validated_data):
        validated_data['create_user'] = self.context
        validated_data['uuid'] = get_uuid()
        Module.objects.create(**validated_data)

        return validated_data


class JobCaseSerializer(serializers.Serializer):
    """测试任务中用例字段序列化器"""

    id = serializers.IntegerField()
    type = serializers.CharField(default='case')
    name = serializers.CharField(source='case_name')


class JobModuleSerializer(serializers.Serializer):
    """测试任务中模块字段序列化器"""

    id = serializers.CharField(source='uuid')
    name = serializers.CharField()
    type = serializers.CharField(default='module')
    subs = JobCaseSerializer(source='cases', many=True)


class JobClientSerializer(serializers.Serializer):
    """测试任务中应用字段序列化器"""

    id = serializers.CharField(source='uuid')
    name = serializers.CharField()
    type = serializers.CharField(default='client')
    subs = JobModuleSerializer(source='modules', many=True)
