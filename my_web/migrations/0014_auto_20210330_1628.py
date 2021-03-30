# Generated by Django 3.1.7 on 2021-03-30 13:28

from django.db import migrations, models
import my_web.models


class Migration(migrations.Migration):

    dependencies = [
        ('my_web', '0013_post_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='unique_id',
            field=models.CharField(default=my_web.models.random_string, max_length=32, unique=True, verbose_name='Уникальный ID'),
        ),
    ]
