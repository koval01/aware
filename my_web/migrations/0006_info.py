# Generated by Django 3.1.4 on 2021-01-10 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_web', '0005_facts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i_title', models.TextField(verbose_name='Title info post')),
                ('i_text', models.TextField(verbose_name='Text info post')),
                ('i_time', models.DateTimeField(verbose_name='Time publish')),
            ],
            options={
                'verbose_name': 'Пост администратора',
                'verbose_name_plural': 'Посты администратора',
            },
        ),
    ]
