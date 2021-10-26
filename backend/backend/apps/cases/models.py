from django.db import models

from backend.utils.models import BaseModel

from users.models import User
from backend.utils.constants import CASE
from backend.utils.helper import get_uuid


class Module(BaseModel):
    """测试系统、模块模型"""

    uuid = models.CharField(max_length=36, verbose_name="UUID", default=get_uuid())
    name = models.CharField(max_length=20, verbose_name="模块名称")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="subs", null=True, blank=True,
                               verbose_name="父级模块")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="modules", verbose_name="创建人")

    class Meta:
        db_table = 'tp_module'
        verbose_name = '模块'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Case(BaseModel):
    """用例模型"""

    no = models.CharField(max_length=120, unique=True, db_index=True, verbose_name="用例编号")
    name = models.CharField(max_length=60, db_index=True, verbose_name="用例名称")
    module = models.ForeignKey(Module, on_delete=models.PROTECT, related_name="cases", verbose_name="功能模块")
    priority = models.SmallIntegerField(choices=CASE['LEVEL'], default=2, verbose_name="优先级")
    status = models.BooleanField(default=True, verbose_name="可用状态")
    is_auto = models.BooleanField(default=False, verbose_name="自动化实现")
    version = models.CharField(max_length=10, null=True, blank=True, verbose_name="A版本号")
    code_time = models.DateTimeField(max_length=24, null=True, blank=True, verbose_name="A编写时间")
    type = models.CharField(max_length=20, null=True, blank=True, verbose_name="A类型")
    author = models.CharField(max_length=20, db_index=True, verbose_name="作者")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sync_cases",
                                verbose_name="同步人")
    reviser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="modify_cases",
                                verbose_name="修改人")

    class Meta:
        db_table = 'tp_case'
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CaseDetail(models.Model):
    """用例详情模型"""

    # 正向查询：当前模型对象.外键字段名  CaseDetail.case
    # 反向查询(未指定relation)：外键模型对象.当前模型类名小写  Case.casedetail
    # 指定了关联名，则同一对多
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="detail", verbose_name="用例")

    description = models.CharField(max_length=100, null=True, blank=True, verbose_name="A用例描述")
    step = models.CharField(max_length=500, null=True, blank=True, verbose_name="测试步骤")
    expectation = models.CharField(max_length=500, null=True, blank=True, verbose_name="测试步骤")
    path = models.CharField(max_length=200, null=True, blank=True, verbose_name="A执行路径")

    class Meta:
        db_table = 'tp_case_detail'
        verbose_name = '用例详情'
        verbose_name_plural = verbose_name
