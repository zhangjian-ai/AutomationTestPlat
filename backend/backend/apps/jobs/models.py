import re

from django.db import models

from backend.utils.models import BaseModel
from backend.utils.constants import JOB
from django.db.models.signals import post_delete
from django.dispatch import receiver
from fdfs_client.exceptions import DataError
from users.models import User
from cases.models import Case
from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage


class Job(BaseModel):
    """测试任务模型"""

    task_no = models.BigIntegerField(unique=True, verbose_name="编号")
    task_name = models.CharField(max_length=100, verbose_name="名称")
    task_detail = models.CharField(max_length=500, null=True, blank=True, verbose_name="详情")
    status = models.SmallIntegerField(choices=JOB['STATUS'], default=0, verbose_name="状态")
    level = models.SmallIntegerField(choices=JOB['LEVEL'], verbose_name="优先级")
    type = models.SmallIntegerField(choices=JOB['TYPE'], verbose_name="类型")
    create_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="create_jobs", verbose_name="创建人")
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="jobs", null=True, blank=True,
                                 verbose_name="责任人")
    prd_no = models.CharField(max_length=80, null=True, blank=True, verbose_name="关联需求编号")
    expect_end_time = models.DateTimeField(verbose_name="预期完成时间")
    actual_end_time = models.DateTimeField(null=True, blank=True, verbose_name="实际完成时间")
    is_delay = models.BooleanField(default=False, verbose_name="延期")
    case = models.ManyToManyField(Case, related_name="jobs", through='JobToCase', through_fields=('job', 'case'),
                                  verbose_name="关联用例")

    class Meta:
        db_table = 'tp_job'
        verbose_name = '测试任务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.task_name}[{self.task_no}]'


class JobToCase(BaseModel):
    """任务用例关联模型"""

    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name="任务")
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name="用例")
    case_status = models.SmallIntegerField(choices=JOB['CASE_STATUS'], default=0, verbose_name="用例状态")
    test_detail = models.CharField(max_length=2000, null=True, blank=True, verbose_name="测试结果详情")

    class Meta:
        db_table = 'tp_job_to_case'
        verbose_name = '任务用例关联表'
        verbose_name_plural = verbose_name


# 删除记录时，同时清除服务器上的文件
@receiver(post_delete, sender=JobToCase)
def delete_storage(sender, **kwargs):
    storage = FastDFSStorage()
    # 匹配出所有file_id
    ids = re.findall(rf'<img src="{storage.base_url}(.+?)">', kwargs['instance'].test_detail)
    for id in ids:
        try:
            storage.delete(id)
        except DataError:
            pass
