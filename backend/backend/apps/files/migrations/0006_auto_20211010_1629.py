# Generated by Django 3.1.7 on 2021-10-10 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_auto_20211010_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(default='', max_length=20, verbose_name='文件名称'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='file',
            name='scope',
            field=models.SmallIntegerField(choices=[(0, 'xmind_template')], unique=True, verbose_name='作用域'),
        ),
        migrations.AlterField(
            model_name='image',
            name='scope',
            field=models.SmallIntegerField(choices=[(0, 'login'), (1, 'logo'), (2, 'auto_true'), (3, 'auto_false'), (4, 'loading')], unique=True, verbose_name='作用域'),
        ),
    ]