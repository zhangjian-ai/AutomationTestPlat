# Generated by Django 3.1.7 on 2022-01-05 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0009_auto_20220105_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='uuid',
            field=models.CharField(default='4ee38ad82031b8366fab851d2ec566ae', max_length=36, verbose_name='UUID'),
        ),
    ]
