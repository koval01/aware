from django.db import models
import string, random


def random_string(min_val=8, max_val=16):
    s = string.ascii_letters + string.digits + '-_'
    x = "".join([random.choice(s) for i in range(random.randrange(min_val, max_val))])
    return x


class Post(models.Model):
    tg_uid = models.CharField('ID пользователя Telegram', max_length=128)
    user_text = models.TextField('Текст пользователя')
    bot_text = models.TextField('Текст бота')
    time_field = models.DateTimeField('Время публикации')
    user_name = models.CharField('Имя пользователя', max_length=255)
    telegraph_page = models.CharField('Telegra.ph страница', max_length=255)
    unique_id = models.CharField('Уникальный ID', max_length=32, unique=True, default=random_string)

    def __str__(self):
        return self.user_text + self.bot_text

    def get_absolute_url(self):
        return "/post/%s/" % self.unique_id

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Quote(models.Model):
    q_text = models.TextField('Текст цитаты')
    q_author = models.CharField('Автор цитаты', max_length=255)
    time = models.DateTimeField('Время публикации')
    unique_id = models.CharField('Уникальный ID', max_length=32, unique=True, default=random_string)

    def __str__(self):
        return self.q_text

    def get_absolute_url(self):
        return "/quote/%s/" % self.unique_id

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'


class Facts(models.Model):
    f_text = models.TextField('Текст факта')
    f_time = models.DateTimeField('Время публикации')
    unique_id = models.CharField('Уникальный ID', max_length=32, unique=True, default=random_string)

    def __str__(self):
        return self.f_text

    def get_absolute_url(self):
        return "/fact/%s/" % self.unique_id

    class Meta:
        verbose_name = 'Факт'
        verbose_name_plural = 'Факты'


class Info(models.Model):
    i_title = models.TextField('Заголовок')
    i_text = models.TextField('Текст поста')
    i_time = models.DateTimeField('Время публикации')

    def __str__(self):
        return self.i_title

    def get_absolute_url(self):
        return "/info/%i/" % self.id

    class Meta:
        verbose_name = 'Пост администратора'
        verbose_name_plural = 'Посты администратора'


class AWARE_Page(models.Model):
    title = models.CharField('Название страницы', max_length=255, default='Не удалось получить заголовок страницы')
    page_html_code = models.TextField('HTML код страницы', default='<p>Ошибка парсинга страницы...</p>')
    unique_id = models.CharField('Уникальный ID', max_length=255, unique=True, default=random_string)

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
    st_time = models.DateTimeField('Время обновления')

    def __str__(self):
        return str(int(self.u_stat) + int(self.b_stat))

    class Meta:
        verbose_name = 'Статистика бота'
        verbose_name_plural = 'Статистика бота'
