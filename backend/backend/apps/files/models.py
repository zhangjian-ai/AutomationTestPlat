from django.db import models

from backend.utils.models import BaseModel
from django.db.models.signals import post_delete
from django.dispatch import receiver

from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage


class Image(BaseModel):
    """系统图片库"""

    IMAGE_TYPE = {
        (1, 'icon'),
        (2, 'background'),
        (3, 'other')
    }

    image = models.ImageField(verbose_name="图片")
    type = models.SmallIntegerField(choices=IMAGE_TYPE, default=3, verbose_name="图片类型")
    location = models.CharField(max_length=20, null=False, unique=True, verbose_name="使用位置")

    class Meta:
        db_table = "tp_image"
        verbose_name = "系统图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.location


# ******************下面的操作是为了在删除数据库数据时，同时删除掉fastDFS里面保存的文件*****************
# 在django管理后台，勾选记录点击执行，delete_model是不会被调用的，只能够在记录编辑界面才可以。坑
# 故解决方案为 在models.py 模型文件中，引入信号机制，执行相关操作
# 在 medels.py中, 引入信号机制，自定义行为,  pre_delete , post_delete , pre_save， post_save等，代码如上
@receiver(post_delete, sender=Image)
def delete_storage(sender, **kwargs):
    storage = FastDFSStorage()
    storage.delete(kwargs['instance'].image.__str__())

