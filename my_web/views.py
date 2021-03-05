from django.template.defaulttags import register
from django.http import HttpResponseForbidden
from django.shortcuts import render
from random import randrange, randint, choice
from .newsapi import __main__ as newsfeed
import logging
import string


logger = logging.getLogger(__name__)


@register.filter
def get_range(value):
    logger.info(f'func get_range: val {value}')
    return randrange(1, value)


@register.filter
def get_randint(value):
    logger.info(f'func get_randint: val {value}')
    return randint(1, value)


@register.filter
def get_range_list(value):
    logger.info(f'func get_range_list: val {value}')
    return range(value)


@register.filter
def cut_text(string):
    logger.info(f'func cut_text: string {string}')
    return string[:256]+'...'


@register.filter
def get_random_string(length = 16):
    letters = string.ascii_letters + string.digits
    return ''.join(choice(letters) for i in range(length))


def index(request):
    logger.info(f'func index: request {request}')
    return render(request, 'my_web/index.html', )


def load_more(request):
    if request.POST:
        logger.info(f'func load_more: request {request}')
        posts = ''
        news = newsfeed()
        return render(request, 'my_web/load_more.html', {'posts': posts, 'news': news},)
    else:
        return HttpResponseForbidden()


def error_400(request, exception):
    logger.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 400. Плохой запрос.'}, )


def error_403(request, exception):
    logger.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 403. Отказано в доступе.'}, )


def error_404(request, exception):
    logger.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )
