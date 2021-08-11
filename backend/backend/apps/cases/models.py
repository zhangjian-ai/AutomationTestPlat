from django.db import models, connection

from backend.utils.models import BaseModel

from users.models import User

from backend.utils.constants import CASE


class Client(BaseModel):
    """测试平台模型"""

    uuid = models.CharField(max_length=36, verbose_name="UUID")
    name = models.CharField(max_length=20, unique=True, verbose_name="应用名称")
    create_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="clients", verbose_name="创建人")

    class Meta:
        db_table = 'tp_application'
        verbose_name = '应用'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Module(BaseModel):
    """测试模块模型"""

    uuid = models.CharField(max_length=36, verbose_name="UUID")
    name = models.CharField(max_length=30, verbose_name="功能模块")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="modules", verbose_name="应用名称")
    create_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="modules", verbose_name="创建人")

    class Meta:
        db_table = 'tp_module'
        verbose_name = '功能模块'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Case(BaseModel):
    """用例模型"""

    case_id = models.CharField(max_length=50, unique=True, verbose_name="用例编号")
    case_name = models.CharField(max_length=50, verbose_name="用例名称")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="cases", verbose_name="应用名称")
    module = models.ForeignKey(Module, on_delete=models.PROTECT, related_name="cases", verbose_name="功能模块")
    level = models.CharField(max_length=1, choices=CASE['LEVEL'], default="M", verbose_name="用例等级")
    owner = models.CharField(max_length=20, verbose_name="用例OWNER")
    updater = models.ForeignKey(User, on_delete=models.PROTECT, related_name="cases", verbose_name="更新人")
    is_auto = models.BooleanField(default=False, verbose_name="自动化实现")
    exec_path = models.CharField(max_length=200, null=True, blank=True, verbose_name="执行路径")
    step = models.CharField(max_length=300, null=True, blank=True, verbose_name="测试步骤")
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name="用例描述")
    version = models.CharField(max_length=10, null=True, blank=True, verbose_name="版本号")
    add_time = models.CharField(max_length=20, null=True, blank=True, verbose_name="用例编写时间")
    status = models.BooleanField(default=True, verbose_name="可用状态")

    class Meta:
        db_table = 'tp_case'
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.case_name

    def lock(self):
        """ Lock table.

        Locks the object model table so that atomic update is possible.
        Simulatenous database access request pend until the lock is unlock()'ed.

        Note: If you need to lock multiple tables, you need to do lock them
        all in one SQL clause and this function is not enough. To avoid
        dead lock, all tables must be locked in the same order.

        See http://dev.mysql.com/doc/refman/5.0/en/lock-tables.html
        """
        cursor = connection.cursor()
        table = self.model._meta.db_table
        cursor.execute("LOCK TABLES %s WRITE" % table)
        row = cursor.fetchone()
        return row

    def unlock(self):
        """ Unlock the table. """
        cursor = connection.cursor()
        cursor.execute("UNLOCK TABLES")
        row = cursor.fetchone()
        return row
