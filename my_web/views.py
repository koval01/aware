import logging
import os
from random import randint, randrange
from time import time

import requests_cache
from cryptography.fernet import Fernet
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit

from .common_functions import get_random_string as rand_str
from .covid.api import covid_api as covid_stat
from .link_analyze import link_image as img_link_check
from .models import AWARE_Page, Facts, Post, Quote, Statistic
from .newsapi import __main__ as newsfeed
from .porfirevich.api import __main__ as porfirevich_strory
from .porfirevich.api import cleanhtml
from .porfirevich.api import get_story as get_story_porfirevich
from .recaptcha_api import get_result as recaptcha_get_result
from .status_api.api import status_api as status_data_api

logger = logging.getLogger(__name__)
image_proxy_key = settings.IMAGE_PROXY_KEY
img_link_proxy_key = settings.IMAGE_PROXY_LINK_KEY
load_more_encrypt_key = settings.LOAD_MORE_ENCRYPT_KEY
qwriter_api_for_aware = os.environ['AWARE_KEY']
img_proxy_session = requests_cache.CachedSession('image_proxy_cache')


@register.filter
def get_range(value) -> int:
    """
    Random range value generator functiontion
    :param value: Input max value
    :return: Output random range value
    """
    logger.info(f'function get_range: {value}')
    return randrange(1, value)


@register.filter
def get_randint(value) -> int:
    """
    Random integer function
    :param value: Input max random value
    :return: Random value result
    """
    logger.info(f'function get_randint: {value}')
    return randint(1, value)


@register.filter
def get_range_list(value) -> range:
    """
    Set range value function
    :param value: Some value set
    :return: Output result
    """
    logger.info(f'function get_range_list: {value}')
    return range(value)


@register.filter
def cut_text(string) -> str:
    """
    String cut function (256 symbols)
    :param string: String for cut
    :return: Cut string result
    """
    logger.info(f'function cut_text: {string}')
    return string[:256]+'...'


@register.filter
def get_item(item) -> print:
    """
    Print data from template function
    :param item: Input data
    :return: return print data
    """
    logger.info(f'function get_item: {item}')
    return print(item)


@register.filter
def get_random_string(length=16) -> str:
    """
    Random string generator function
    :param length: length string
    :return: generated string
    """
    return rand_str(length)


@register.filter
def link_encrypt_img(link) -> str:
    """
    Link encryptor
    :param link: Link image
    :return: Encrypted link
    """
    try:
        salt_link = Fernet(img_link_proxy_key)
        data_link = str.encode(str(link))
        result = salt_link.encrypt(data_link).decode("utf-8")
        return result
    except Exception as e:
        logger.error(e)


@ratelimit(key='header:X-Forwarded-For', rate='90/m', block=True)
def image_proxy_view(request):
    """
    Image proxy function
    :param request: body request
    :return: raw image
    """
    if request.GET:
        try:
            url = request.GET['data']
            salt_link = Fernet(img_link_proxy_key)
            link_get = salt_link.decrypt(str.encode(str(url))).decode('utf-8')
            if img_link_check(link_get):
                token = request.GET['token']
                salt = Fernet(image_proxy_key)
                token_get = int(salt.decrypt(str.encode(str(token))).decode('utf-8')) + 60
                control_time = round(time())
                if token_get > control_time:
                        response = img_proxy_session.get(
                            link_get, stream=True,
                            headers={'user-agent': request.headers.get('user-agent')}
                        )
                        return StreamingHttpResponse(
                            response.raw,
                            content_type=response.headers.get('content-type'),
                            status=response.status_code,
                            reason=response.reason,
                        )
        except Exception as e:
            logger.error(e)

    return error_403(request)


@csrf_exempt
@ratelimit(key='header:X-Forwarded-For', rate='100/m', block=True)
def aware_api(request):
    """
    API for AWARE
    :param request: body request
    :return: json answer
    """
    if request.POST:
        token_get = request.POST.get('api_key', '')
        token = qwriter_api_for_aware
        if token == token_get:
            try:
                title = request.POST.get('title', '')
                page_html_code = request.POST.get('page_html_code', '')
                if title and page_html_code:
                    logger.info('AWARE API Title: %s' % title)
                    logger.info('AWARE API HTML: %s' % page_html_code)
                    a = AWARE_Page(title=title, page_html_code=page_html_code)
                    a.save()
                    return JsonResponse(
                        {
                            'done': True,
                            'unique_id': a.unique_id,
                        }
                    )
            except Exception as e:
                logger.error(e)
                return JsonResponse(
                    {
                        'done': False,
                        'exception': e,
                    }, status=409
                )
        else:
            return JsonResponse(
                {
                    'done': False,
                    'exception': 'Unauthorized',
                }, status=401
            )

    return error_403(request)


@ratelimit(key='header:X-Forwarded-For', rate='40/m', block=True)
def index(request):
    """
    Index page view
    :param request: request body
    :return: render template page
    """
    # unix time mark encryption
    salt = Fernet(load_more_encrypt_key)
    data = str.encode(str(round(time())))
    token_valid = salt.encrypt(data).decode("utf-8")
    token_re = settings.RETOKEN_PUBLIC

    logger.info(f'function index: request {request}')
    return render(request, 'my_web/index.html', {
        'token_valid': token_valid, 'token_re': token_re,
    })


@ratelimit(key='header:X-Forwarded-For', rate='15/m', block=True)
def news_feed(request):
    """
    News page view
    :param request: request body
    :return: render template page
    """
    # unix time mark encryption
    salt = Fernet(load_more_encrypt_key)
    data = str.encode(str(round(time())))
    token_valid = salt.encrypt(data).decode("utf-8")
    token_re = settings.RETOKEN_PUBLIC

    logger.info(f'function index: request {request}')
    return render(request, 'my_web/news-feed.html', {
        'token_valid': token_valid, 'token_re': token_re,
    })


@ratelimit(key='header:X-Forwarded-For', rate='5/m', block=True)
def status(request):
    """
    Status page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function index: request {request}')
    status_data = status_data_api()
    return render(request, 'my_web/status.html', {'status': status_data})


@ratelimit(key='header:X-Forwarded-For', rate='15/m', block=True)
def botpage(request):
    """
    Bot info page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function index: request {request}')
    return render(request, 'my_web/botpage.html', )


@ratelimit(key='header:X-Forwarded-For', rate='15/m', block=True)
def info(request):
    """
    Info site page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function info: request {request}')
    return render(request, 'my_web/info.html')


@ratelimit(key='header:X-Forwarded-For', rate='10/m', block=True)
def postview(request, postid):
    """
    Post page view
    :param postid: searching post id
    :param request: request body
    :return: render template page
    """
    logger.info(f'function postview: request {request}; postid {postid}')
    try:
        postid: request.GET.get('postid', '')
        for p in Post.objects.raw('SELECT * FROM my_web_post WHERE unique_id = "{}" LIMIT 1'.format(postid)):
            post = p
        return render(request, 'my_web/postview.html', {'postget': post})
    except Exception as e:
        return error_404(request, e)


@ratelimit(key='header:X-Forwarded-For', rate='10/m', block=True)
def storyview(request, storyid):
    """
    Story page view
    :param storyid: searching story id
    :param request: request body
    :return: render template page
    """
    logger.info(f'function storyview: request {request}; storyid {storyid}')
    try:
        storyid: request.GET.get('storyid', '')
        if not get_story_porfirevich(storyid):
            return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, status=404)

        text, time, likes, id_s = get_story_porfirevich(storyid)
        t = cleanhtml(text)
        short_text = t
        if len(text) > 1000:
            short_text = short_text[:1000] + '...'
        return render(request, 'my_web/storyview.html', {
            'text': text, 'time': time,
            'likes': likes, 'id_s': id_s, 'short_text': short_text
        })
    except Exception as e:
        return error_404(request, e)


@ratelimit(key='header:X-Forwarded-For', rate='10/m', block=True)
def quoteview(request, quoteid):
    """
    Quote page view
    :param quoteid: searching quote id
    :param request: request body
    :return: render template page
    """
    logger.info(f'function quoteview: request {request}; quoteid {quoteid}')
    try:
        postid: request.GET.get('postid', '')
        for q in Quote.objects.raw('SELECT * FROM my_web_quote WHERE unique_id = "{}" LIMIT 1'.format(quoteid)):
            quote = q
        return render(request, 'my_web/quoteview.html', {'quoteget': quote})
    except Exception as e:
        return error_404(request, e)


@ratelimit(key='header:X-Forwarded-For', rate='10/m', block=True)
def factview(request, factid):
    """
    Fact page view
    :param factid: searching fact id
    :param request: request body
    :return: render template page
    """
    logger.info(f'function factview: request {request}; factid {factid}')
    try:
        factid: request.GET.get('factid', '')
        for f in Facts.objects.raw('SELECT * FROM my_web_facts WHERE unique_id = "{}" LIMIT 1'.format(factid)):
            fact = f
        return render(request, 'my_web/factview.html', {'factget': fact})
    except Exception as e:
        logger.error(e)
        return error_404(request, e)


@ratelimit(key='header:X-Forwarded-For', rate='20/m', block=True)
def awareview(request, awareid):
    """
    AWARE page view
    :param awareid: searching fact id
    :param request: request body
    :return: render template page
    """
    logger.info(f'function awareview: request {request}; awareid {awareid}')
    try:
        awareid: request.GET.get('awareid', '')
        for a in AWARE_Page.objects.raw('SELECT * FROM my_web_aware_page WHERE unique_id = "{}" LIMIT 1'.format(awareid)):
            aware = a
        return render(request, 'my_web/awareview.html', {'aware': aware})
    except Exception as e:
        logger.error(e)
        return error_404(request, e)


@ratelimit(key='header:X-Forwarded-For', rate='5/m', block=True)
def stats(request):
    """
    Statistics page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function stats: request {request}')
    try:
        for s in Statistic.objects.raw('SELECT * FROM my_web_statistic LIMIT 1'):
            stat = s
        sumstat = str(int(stat.u_stat) + int(stat.b_stat))
        return render(request, 'my_web/stats.html', {'statget': stat, 'sumstat': sumstat}, )
    except Exception as e:
        return error_404(request, e)


@ratelimit(key='header:X-Forwarded-For', rate='50/m', block=True)
def load_more(request):
    """
    Technical (load_more) page view
    :param request: request body
    :return: render template page
    """
    if request.POST:
        # get params
        try:
            token = request.POST.get('validtoken', '')
            typeload = request.POST.get('typeload', '')
            r_token = request.POST.get('gr_token', '')
        except Exception as e:
            token = 0;typeload = 0;r_token = 0
            logging.error(e)

        if recaptcha_get_result(r_token):

            additions = int(request.POST.get('additions', ''))
            news_append = int(request.POST.get('news', ''))

            if token and typeload:
                if typeload == 'newsession':
                    covid_stat_ua = covid_stat('UA')
                    covid_stat_ru = covid_stat('RU')
                else:
                    covid_stat_ua = 0
                    covid_stat_ru = 0

                # token decrypt
                try:
                    salt = Fernet(load_more_encrypt_key)
                    token_get = int(salt.decrypt(str.encode(str(token))).decode('utf-8'))
                except Exception as e:
                    token_get = 0
                    logging.error(e)

                if token_get and (token_get + 1800) > round(time()):
                    # data collect
                    stories = porfirevich_strory()
                    posts = Post.objects.order_by('?')[:20]
                    quotes = Quote.objects.order_by('?')[:20]
                    facts = Facts.objects.order_by('?')[:20]
                    news = newsfeed(news_append)

                    # image proxy encrypt data
                    salt = Fernet(image_proxy_key)
                    data = str.encode(str(round(time())))
                    token_valid = salt.encrypt(data).decode("utf-8")

                    # data pack
                    data = zip(stories, posts, quotes, facts, news)

                    logger.info(f'function load_more: request {request}')

                    return render(request, 'my_web/load_more.html', {
                        'data': data, 'token_image_proxy': token_valid,
                        'typeload': typeload, 'covid_ru': covid_stat_ru,
                        'covid_ua': covid_stat_ua, 'additions': additions,
                        'news_append': news_append,
                    })

    return error_403(request)


def error_400(request, exception='Unknown'):
    """
    400 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    logger.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 400. Плохой запрос.'}, status=400)


def error_403(request, exception='Unknown'):
    """
    403 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    logger.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 403. Отказано в доступе.'}, status=403)


def error_404(request, exception='Unknown'):
    """
    404 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    logger.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, status=404)
