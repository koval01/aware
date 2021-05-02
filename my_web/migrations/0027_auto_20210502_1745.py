# Generated by Django 3.2 on 2021-05-02 14:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('my_web', '0026_auto_20210429_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aware_page',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 14, 45, 38, 505663, tzinfo=utc), verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='info',
            name='i_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 14, 45, 38, 427539, tzinfo=utc), verbose_name='Время публикации'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='st_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 14, 45, 38, 505663, tzinfo=utc), verbose_name='Время обновления'),
        ),
    ]