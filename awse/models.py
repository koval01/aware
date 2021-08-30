import random
import string

from bs4 import BeautifulSoup
from django.db import models
from django.utils import timezone

from awse.other.common_functions import num_formatter


def random_string():
    s = string.ascii_letters + string.digits + '-_'
    x = "".join([random.choice(s) for i in range(random.randrange(10, 20))])
    return x


class Info(models.Model):
    # Choice lists
    SELECT_LANGUAGE = [
        ('ua', 'Ukrainian'),
        ('ru', 'Russian'),
        ('en', 'English'),
    ]
    SELECT_ACTIVE_MODE = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    i_text = models.TextField('Text')
    i_language = models.CharField('Language', choices=SELECT_LANGUAGE, default='ru', max_length=2)
    i_active = models.CharField('Actively', choices=SELECT_ACTIVE_MODE, default='yes', max_length=3)
    i_chance = models.IntegerField('Display chance (1 to 100)', max_length=3)
    i_views = models.PositiveIntegerField('Views', default=0, editable=False)
    i_time_active = models.DateTimeField('Active until', default=timezone.now())

    def __str__(self):
        title = BeautifulSoup(self.i_text, 'lxml').text
        views = self.i_views
        if len(title) > 30:
            title = "%s..." % str(title[:30]).rstrip()
        return "%s (Views: %s)" % (title, num_formatter(views))

    class Meta:
        verbose_name = 'Advertising record'
        verbose_name_plural = 'Advertising records'


class Banner(models.Model):
    # Choice lists
    SELECT_ACTIVE_MODE = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    text = models.CharField('Text', max_length=255)
    active = models.CharField('Actively', choices=SELECT_ACTIVE_MODE, default='yes', max_length=3)
    chance = models.IntegerField('Display chance (1 to 100)', max_length=3)
    link_image = models.TextField('Image link')
    link_site = models.CharField('Site domain (Example - awse.us or awse.us/page/second_page)', max_length=255)
    utm_source = models.CharField('UTM Source', max_length=255, default='null')
    utm_medium = models.CharField('UTM Medium', max_length=255, default='null')
    utm_campaign = models.CharField('UTM Campaign', max_length=255, default='null')
    utm_content = models.CharField('UTM Content', max_length=255, default='null')
    utm_term = models.CharField('UTM Term', max_length=255, default='null')
    views = models.PositiveIntegerField('Views', default=0, editable=False)
    time_active = models.DateTimeField('Active until', default=timezone.now())

    def __str__(self):
        title = BeautifulSoup(self.text, 'lxml').text
        views = self.views
        if len(title) > 30:
            title = "%s..." % str(title[:30]).rstrip()
        return "%s (Views: %s)" % (title, num_formatter(views))

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'


class AWSE_Page(models.Model):
    title = models.CharField('Page title', max_length=255, default='Failed to get page title')
    page_html_code = models.TextField('HTML code of the page', default='<p>Page parsing error ...</p>')
    unique_id = models.CharField('Unique ID', max_length=255, unique=True, default=random_string)
    time = models.DateTimeField('Time of creation', default=timezone.now())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/awse/%s/" % self.unique_id

    class Meta:
        verbose_name = 'AWSE page'
        verbose_name_plural = 'AWSE Pages'


class BlackWord(models.Model):
    SELECT_MODE = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    word = models.CharField('Word', max_length=255, unique=True)
    ano_mode = models.CharField('Anagram', choices=SELECT_MODE, default='yes', max_length=3)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        for field_name in ['word']:
            value = getattr(self, field_name, False)
            if value:
                setattr(self, field_name, value.capitalize())
        super(BlackWord, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Black word'
        verbose_name_plural = 'Black words'


class Statistic(models.Model):
    u_stat = models.IntegerField('User statistics')
    b_stat = models.IntegerField('Bot statistics')
    st_time = models.DateTimeField('Update time', default=timezone.now())

    def __str__(self):
        return str(int(self.u_stat) + int(self.b_stat))

    class Meta:
        verbose_name = 'Bot statistics'
        verbose_name_plural = 'Bot statistics'
