import random
from datetime import datetime

from rest_framework import serializers

from cases.models import Case
from .models import Job, JobToCase
from cases.serializer import CaseSerializer


class JobSerializer(serializers.ModelSerializer):
    """测试任务序列化器"""
    # 新增用例时有用例列表
    case = serializers.ListField(label="用例ID集", write_only=True)

    # 序列化用例列表时，借用用例本身的序列化器。
    # 当任务较多时，序列化任务列表的用例相当费时，固查询任务时暂序列化出用例
    # case_list = CaseSerializer(source='case', read_only=True, many=True)

    # 时间字段格式化
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    expect_end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    actual_end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)

    # chioce字段 get_<字段名>_display 显示名称
    level_str = serializers.CharField(source='get_level_display', read_only=True)
    status_str = serializers.CharField(source='get_status_display', read_only=True)
    type_str = serializers.CharField(source='get_type_display', read_only=True)

    # 获取外键的str。字符类型序列化器，来源是外键对象时，默认返回对象的__str__()
    create_user_name = serializers.CharField(source='create_user', read_only=True)
    executor_name = serializers.CharField(source='executor', read_only=True, default="无")

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('id', 'task_no', 'create_user')

    def validate(self, attrs):
        # 相同名称的任务不允许创建
        task_name = attrs.get('task_name')
        try:
            Job.objects.get(task_name=task_name)
        except Job.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('同名的测试任务已被创建')

    def create(self, validated_data):
        # 添加无默认值的只读字段
        validated_data['task_no'] = '{0:%Y%m%d%H%M%S}'.format(datetime.now()) + str(random.randint(1000, 9999))
        validated_data['create_user'] = self.context

        # 取出用例id列表
        ids = validated_data.pop('case')

        # 创建任务对象
        job = Job.objects.create(**validated_data)

        # 获取到用例查询集
        caseSet = Case.objects.filter(id__in=ids)

        # 任务绑定用例
        job.case.add(*caseSet)

        return job


class JobToCaseSerializer(serializers.ModelSerializer):
    """用例执行详情序列化器"""

    case_status_str = serializers.CharField(source='get_case_status_display', read_only=True)
    test_detail = serializers.CharField(allow_null=True, required=False)
    case = CaseSerializer(read_only=True)

    class Meta:
        model = JobToCase
        exclude = ('create_time', 'update_time')
