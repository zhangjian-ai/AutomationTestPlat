from rest_framework import serializers

from .models import Case, CaseDetail, Module


class CaseSerializer(serializers.ModelSerializer):
    """用例序列化器"""

    # 用例详情字段
    description = serializers.CharField(max_length=100, allow_null=True, required=False, write_only=True, label="用例描述")
    expectation = serializers.CharField(max_length=100, allow_null=True, required=False, write_only=True, label="测试步骤")
    step = serializers.CharField(max_length=250, allow_null=True, required=False, write_only=True, label="测试步骤")
    path = serializers.CharField(max_length=200, allow_null=True, required=False, write_only=True, label="A执行路径")

    # chioce字段 get_<字段名>_display 显示名称
    priority_str = serializers.CharField(source='get_priority_display', read_only=True)

    # 时间字段格式优化
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    code_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    # 模块名称级联展示
    module_str3 = serializers.CharField(source='module', read_only=True)
    module_str2 = serializers.CharField(source='module.parent', read_only=True)
    module_str1 = serializers.CharField(source='module.parent.parent', read_only=True)

    # 修改人名称
    reviser_str = serializers.CharField(source='reviser', read_only=True)

    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = ['status']

    def validate(self, attrs):
        # 自动化用例exec_path不能为空
        if attrs.get('is_auto'):
            if not attrs.get('path'):
                return serializers.ValidationError('is_auto为true时，path必填')
        return attrs

    def create(self, validated_data):
        # 剥离出用例详情字段
        detail = {
            'description': validated_data.pop('description', None),
            'expectation': validated_data.pop('expectation', None),
            'step': validated_data.pop('step', None),
            'path': validated_data.pop('path', None)
        }

        # 创建用例
        case = Case.objects.create(**validated_data)

        # 创建对应的用例详情
        detail['case'] = case
        CaseDetail.objects.create(**detail)

        return case


class CaseDetailSerializer(serializers.ModelSerializer):
    """用例详情序列化器"""

    class Meta:
        model = CaseDetail
        exclude = ['id', 'case']


class SubSerializer(serializers.Serializer):
    """子模块递归序列化实现"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ModuleSerializer(serializers.ModelSerializer):
    """功能模块序列化器"""

    # 自关联子类对象
    subs = SubSerializer(many=True, read_only=True)
    # 父类名称
    parent_str = serializers.CharField(source='parent', read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'name', 'parent', 'parent_str', 'subs']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['creator'] = self.context
        module = Module.objects.create(**validated_data)
        return module


class SimpleCaseSerializer(serializers.Serializer):
    """简单用例信息序列化器"""

    id = serializers.IntegerField()
    cate = serializers.CharField(default='case')
    name = serializers.CharField()


class CaseTreeSerializer(serializers.Serializer):
    """树形用例列表序列化器"""

    id = serializers.CharField()
    name = serializers.CharField()
    cate = serializers.CharField(default='module')
    subs = SubSerializer(many=True)
    cases = SimpleCaseSerializer(many=True)
