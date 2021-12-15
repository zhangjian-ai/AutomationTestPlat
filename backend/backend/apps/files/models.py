from django.db import models

from backend.utils.models import BaseModel
from backend.utils.constants import RESOURCE
from django.db.models.signals import post_delete
from django.dispatch import receiver

from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage
from fdfs_client.exceptions import DataError


class Image(BaseModel):
    """系统图片库"""

    image = models.ImageField(verbose_name="图片地址")
    scope = models.SmallIntegerField(choices=RESOURCE['IMAGE'], unique=True, verbose_name="作用域")

    class Meta:
        db_table = "tp_image"
        verbose_name = "系统图片"
        verbose_name_plural = verbose_name


class File(BaseModel):
    """系统文件库"""
    file = models.FileField(verbose_name="文件地址")
    name = models.CharField(max_length=20, verbose_name="文件名称")
    scope = models.SmallIntegerField(choices=RESOURCE['FILE'], unique=True, verbose_name="作用域")

    class Meta:
        db_table = "tp_file"
        verbose_name = "系统文件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SourceModel(BaseModel):
    """系统资源库"""
    uid = models.BigIntegerField(verbose_name="UID")
    name = models.CharField(max_length=250, verbose_name="资源名称")
    os = models.CharField(max_length=12, verbose_name="操作系统")
    version = models.CharField(max_length=20, verbose_name="版本")
    size = models.CharField(max_length=10, verbose_name="文件大小")
    size_bytes = models.BigIntegerField(verbose_name="文件大小(字节)", default=0)
    file_id = models.CharField(max_length=200, verbose_name="资源路径")
    author = models.CharField(max_length=20, verbose_name="贡献者")

    class Meta:
        db_table = "tp_source"
        verbose_name = "系统资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# ******************下面的操作是为了在删除数据库数据时，同时删除掉fastDFS里面保存的文件*****************
# 在django管理后台，勾选记录点击执行，delete_model是不会被调用的，只能够在记录编辑界面才可以。坑
# 故解决方案为 在models.py 模型文件中，引入信号机制，执行相关操作
# 在 medels.py中, 引入信号机制，自定义行为,  pre_delete , post_delete , pre_save， post_save等，代码如上
@receiver(post_delete, sender=Image)
def delete_storage(sender, **kwargs):
    storage = FastDFSStorage()
    storage.delete(kwargs['instance'].image.__str__())


@receiver(post_delete, sender=File)
def delete_storage(sender, **kwargs):
    storage = FastDFSStorage()
    storage.delete(kwargs['instance'].file.__str__())


@receiver(post_delete, sender=SourceModel)
def delete_storage(sender, **kwargs):
    try:
        storage = FastDFSStorage()
        storage.delete(kwargs['instance'].file_id)
    except DataError:
        pass
