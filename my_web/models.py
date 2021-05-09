from django.db import models
from django.utils import timezone
import string, random


def random_string():
    s = string.ascii_letters + string.digits + '-_'
    x = "".join([random.choice(s) for i in range(random.randrange(10, 20))])
    return x


class Info(models.Model):
    SELECT_LANGUAGE = [
        ('ua', 'Украинский'),
        ('ru', 'Русский'),
        ('en', 'Английский'),
    ]

    i_title = models.CharField('Заголовок', max_length=255, default='Рекламная запись')
    i_text = models.TextField('Текст')
    i_language = models.CharField('Язык', choices=SELECT_LANGUAGE, default='ru', max_length=2)
    i_chance = models.IntegerField('Шанс отображения (от 1 до 100)', max_length=3)
    i_time_active = models.DateTimeField('Активно до', default=timezone.now())

    def __str__(self):
        return self.i_title

    class Meta:
        verbose_name = 'Рекламная запись'
        verbose_name_plural = 'Рекламные записи'


class AWARE_Page(models.Model):
    title = models.CharField('Название страницы', max_length=255, default='Не удалось получить заголовок страницы')
    page_html_code = models.TextField('HTML код страницы', default='<p>Ошибка парсинга страницы...</p>')
    unique_id = models.CharField('Уникальный ID', max_length=255, unique=True, default=random_string)
    time = models.DateTimeField('Время создания', default=timezone.now())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/aware/%s/" % self.unique_id

    class Meta:
        verbose_name = 'Страница AWARE'
        verbose_name_plural = 'Страницы AWARE'


class Statistic(models.Model):
    u_stat = models.IntegerField('Стастика пользователей')
    b_stat = models.IntegerField('Статистика бота')
    st_time = models.DateTimeField('Время обновления', default=timezone.now())

    def __str__(self):
        return str(int(self.u_stat) + int(self.b_stat))

    class Meta:
        verbose_name = 'Статистика бота'
        verbose_name_plural = 'Статистика бота'
