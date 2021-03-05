# Generated by Django 3.1.4 on 2021-01-03 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_uid', models.CharField(max_length=128, verbose_name='Telegram user ID')),
                ('user_text', models.TextField(verbose_name='Text by user')),
                ('bot_text', models.TextField(verbose_name='Text by bot')),
                ('time', models.TextField(verbose_name='Time publish')),
                ('user_name', models.TextField(verbose_name='User name')),
                ('telegraph_page', models.TextField(verbose_name='Telegra.ph page')),
            ],
        ),
    ]
