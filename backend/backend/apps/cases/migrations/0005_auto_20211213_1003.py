# Generated by Django 3.1.7 on 2021-12-13 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0004_auto_20211212_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='uuid',
            field=models.CharField(default='d33f9171fdbe3368670b21d23fbfee6f', max_length=36, verbose_name='UUID'),
        ),
    ]
