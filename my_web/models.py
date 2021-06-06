from django.db import models
from django.utils import timezone
from bs4 import BeautifulSoup
from .common_functions import num_formatter
import string, random


def random_string():
    s = string.ascii_letters + string.digits + '-_'
    x = "".join([random.choice(s) for i in range(random.randrange(10, 20))])
    return x


class Info(models.Model):
    # Choice lists
    SELECT_LANGUAGE = [
        ('ua', 'Украинский'),
        ('ru', 'Русский'),
        ('en', 'Английский'),
    ]
    SELECT_ACTIVE_MODE = [
        ('yes', 'Да'),
        ('no', 'Нет'),
    ]

    i_text = models.TextField('Текст')
    i_language = models.CharField('Язык', choices=SELECT_LANGUAGE, default='ru', max_length=2)
    i_active = models.CharField('Активно', choices=SELECT_ACTIVE_MODE, default='yes', max_length=3)
    i_chance = models.IntegerField('Шанс отображения (от 1 до 100)', max_length=3)
    i_views = models.PositiveIntegerField('Просмотры', default=0, editable=False)
    i_time_active = models.DateTimeField('Активно до', default=timezone.now())

    def __str__(self):
        title = BeautifulSoup(self.i_text, 'lxml').text
        views = self.i_views
        if len(title) > 30:
            title = "%s..." % str(title[:30]).rstrip()
        return "%s (Просмотров: %s)" % (title, num_formatter(views))

    class Meta:
        verbose_name = 'Рекламная запись'
        verbose_name_plural = 'Рекламные записи'


class Banner(models.Model):
    # Choice lists
    SELECT_ACTIVE_MODE = [
        ('yes', 'Да'),
        ('no', 'Нет'),
    ]

    text = models.TextField('Текст')
    active = models.CharField('Активно', choices=SELECT_ACTIVE_MODE, default='yes', max_length=3)
    chance = models.IntegerField('Шанс отображения (от 1 до 100)', max_length=3)
    link_image = models.TextField('Ссылка на изображение')
    link_site = models.TextField('Домен сайта (Пример - awse.us)')
    utm_source = models.CharField('UTM Source', max_length=255)
    utm_medium = models.CharField('UTM Medium', max_length=255)
    utm_campaign = models.CharField('UTM Campaign', max_length=255)
    utm_content = models.CharField('UTM Content', max_length=255)
    utm_term = models.CharField('UTM Term', max_length=255)
    views = models.PositiveIntegerField('Просмотры', default=0, editable=False)
    time_active = models.DateTimeField('Активно до', default=timezone.now())

    def __str__(self):
        title = BeautifulSoup(self.text, 'lxml').text
        views = self.views
        if len(title) > 30:
            title = "%s..." % str(title[:30]).rstrip()
        return "%s (Просмотров: %s)" % (title, num_formatter(views))

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


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


class BlackWord(models.Model):
    SELECT_MODE = [
        ('yes', 'Да'),
        ('no', 'Нет'),
    ]

    word = models.CharField('Слово', max_length=255, unique=True)
    ano_mode = models.CharField('Анаграмма', choices=SELECT_MODE, default='yes', max_length=3)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        for field_name in ['word']:
            value = getattr(self, field_name, False)
            if value:
                setattr(self, field_name, value.capitalize())
        super(BlackWord, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Черное слово'
        verbose_name_plural = 'Черные слова'


class Statistic(models.Model):
    u_stat = models.IntegerField('Стастика пользователей')
    b_stat = models.IntegerField('Статистика бота')
    st_time = models.DateTimeField('Время обновления', default=timezone.now())

    def __str__(self):
        return str(int(self.u_stat) + int(self.b_stat))

    class Meta:
        verbose_name = 'Статистика бота'
        verbose_name_plural = 'Статистика бота'
