# Generated by Django 3.2.2 on 2021-05-09 13:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('my_web', '0031_auto_20210509_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aware_page',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 9, 13, 28, 22, 68619, tzinfo=utc), verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='info',
            name='i_language',
            field=models.CharField(choices=[('ua', 'Украинский'), ('ru', 'Русский'), ('en', 'Английский')], default='ru', max_length=2, verbose_name='Язык'),
        ),
        migrations.AlterField(
            model_name='info',
            name='i_time_active',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 9, 13, 28, 21, 984614, tzinfo=utc), verbose_name='Активно до'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='st_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 9, 13, 28, 22, 68619, tzinfo=utc), verbose_name='Время обновления'),
        ),
    ]
