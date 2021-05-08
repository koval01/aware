import logging
import os
import random
from datetime import timedelta
from multiprocessing import Process
from random import randint, randrange
from time import time
from urllib.parse import urlunsplit, urlencode

from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from requests import get

from .awareapi_filter import get_instant_page as instant_aware
from .calculate import calculator
from .common_functions import get_random_string as rand_str
from .covid.api import covid_api as covid_stat
from .covid.api import num_formatter
from .deepl import translate_simple
from .get_search_template import get_result as search_example
from .infobot.core import send_data as infobot_send_data
from .link_analyze import link_image as img_link_check
from .load_text import get_text as loading_button_text
from .models import AWARE_Page
from .namaz_api import get_namaz_data
from .newsapi import __main__ as newsfeed
from .newsapi import news_search as news_search_in_str
from .randstuff_api import get_result as rand_fact_or_quote
from .recaptcha_api import get_result as recaptcha_get_result
from .search_api import select_type as search_execute
from .search_complete_api import get_result_data as search_complete
from .status_api.api import status_api as status_data_api
from .telegram_controller.bot_script import heart as telegram_bot
from .text_to_image_api import get_result as text_to_image_api
from .text_to_image_api import sentence_check
from .tiktok_static import get_data as tiktok_data_get

logger = logging.getLogger(__name__)
image_proxy_key = settings.IMAGE_PROXY_KEY
img_link_proxy_key = settings.IMAGE_PROXY_LINK_KEY
load_more_encrypt_key = settings.LOAD_MORE_ENCRYPT_KEY
bot_check_tk = settings.BOT_CHECK_TOKEN
sign_key = settings.SIGN_ENCRYPT_KEY
qwriter_api_for_aware = os.environ['AWARE_KEY']


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
    return string[:256] + '...'


@register.filter
def seconds_to_time(val) -> str:
    """
    Convert seconds to time XX:XX:XX
    :param val: seconds int
    :return: string time
    """
    return str(timedelta(seconds=val))


@register.filter
def get_item(item) -> print:
    """
    Print data from template function
    :param item: Input data
    :return: return print data
    """
    print(item)
    return item


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
    :param link: Link image / video
    :return: Encrypted link
    """
    try:
        salt_link = Fernet(img_link_proxy_key)
        data_link = str.encode(str(link))
        result = salt_link.encrypt(data_link).decode("utf-8")
        return result
    except Exception as e:
        logger.error(e)


@register.filter
def num_rounder_custom(val) -> str:
    """
    Round value to K, M...
    :param val: int value
    :return: string rounded value
    """
    return num_formatter(val)


@register.filter
def sign_address_encrypt(address) -> str:
    """
    Address encryptor
    :param address: User address
    :return: Encrypted address
    """
    try:
        salt_sign = Fernet(sign_key)
        data_sign = str.encode(str(address))
        result = salt_sign.encrypt(data_sign).decode("utf-8")
        return result
    except Exception as e:
        logger.error(e)


@require_GET
def image_proxy_view(request):
    """
    Image proxy function
    :param request: body request
    :return: raw image
    """
    try:
        salt = Fernet(sign_key)
        original_address = request.headers['X-Forwarded-For'].replace(' ', '').split(',')[0]
        received_address = salt.decrypt(str.encode(str(request.GET['sign']))).decode('utf-8')
        if original_address == received_address:
            try:
                video = request.GET['video_mode']
            except Exception as e:
                video = False
                logger.warning(e)
            url = request.GET['data']
            salt_link = Fernet(img_link_proxy_key)
            link_get = salt_link.decrypt(str.encode(str(url))).decode('utf-8')
            if img_link_check(link_get, video=video):
                token = request.GET['token']
                salt = Fernet(image_proxy_key)
                token_get = int(salt.decrypt(str.encode(str(token))).decode('utf-8')) + 15
                control_time = round(time())
                if token_get > control_time:
                    response = get(
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

    return error_400(request)


@require_GET
@cache_page(60 * 180)
def image_generate_api(request):
    """
    Image to text api
    :param request: body request
    :return: raw image
    """
    salt = Fernet(sign_key)
    original_address = request.headers['X-Forwarded-For'].replace(' ', '').split(',')[0]
    received_address = salt.decrypt(str.encode(str(request.GET['sign']))).decode('utf-8')
    if original_address == received_address:
        token = request.GET['token']
        salt = Fernet(image_proxy_key)
        token_get = int(salt.decrypt(str.encode(str(token))).decode('utf-8')) + 15
        control_time = round(time())
        if token_get > control_time:
            try:
                text = request.GET['text']
                author = request.GET['author']
                if 5 < len(text) <= 1000 and 2 < len(author) <= 64:
                    logger.info('IMAGE GENERATOR: Check sentences')
                    if not sentence_check(text):
                        return JsonResponse(
                            {
                                'code': 409, 'code_name': 'Conflict',
                                'error': 'This text does not seem to have any value.',
                            }
                        )
                    logger.info('IMAGE GENERATOR: Generating image')
                    img = text_to_image_api(text, author)
                    logger.info('IMAGE GENERATOR: Sending image to user')
                    return HttpResponse(
                        img['img'],
                        content_type=img['headers'],
                        status=img['status_code'],
                        reason=img['reason'],
                    )
                return JsonResponse(
                    {
                        'code': 411, 'code_name': 'Length Required',
                        'error': 'Text length cannot be less than 5 characters or more than 1000. The author\'s name / nickname cannot be shorter than 2 characters and longer than 64 characters.',
                    }
                )
            except Exception as e:
                logger.error(e)

    return error_400(request)


@require_GET
@cache_page(60 * 180)
def search_suggestions_get(request):
    """
    We receive search suggestions
    :param request: request body
    :return: list suggestions
    """
    try:
        q = request.GET['q']
        if q and len(q) < 110:
            return JsonResponse({"data": search_complete(q)})
    except Exception as e:
        logger.error(e)

    return error_400(request)


@require_POST
@csrf_exempt
def bot_gateway(request, token):
    """
    Telegram bot gateway view
    :param request: request body
    :param token: Secret token
    :return: response body
    """
    token: request.GET.get('token', '')
    if token == bot_check_tk:
        telegram_bot(request.read().decode("utf-8"))
        return HttpResponse('True')
    return error_400(request)


@require_POST
@csrf_exempt
def aware_api(request):
    """
    API for AWARE
    :param request: body request
    :return: json answer
    """
    token_get = request.POST.get('api_key', '')
    token = qwriter_api_for_aware
    if token == token_get:
        try:
            link = str(request.POST.get('link', ''))
            if link:
                data = instant_aware(link)
                a = AWARE_Page(title=data['title'], page_html_code=data['html'])
                a.save()
                page_id = AWARE_Page.objects.latest('id').unique_id
                query = urlencode(dict(
                    url='https://awse.us/aware/' + page_id,
                    rhash=data['template'],
                ))
                link = urlunsplit(('https', 't.me', '/iv', query, ''))
                return JsonResponse(
                    {
                        'done': True,
                        'link': link,
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

    return error_400(request)


@require_GET
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

    search_example_get = search_example()
    search_example_get = BeautifulSoup(
        search_example_get, 'lxml'
    ).text

    r_type = random.randint(0, 1)
    add_ = rand_fact_or_quote(r_type)

    logger.info(f'function index: request {request}')
    return render(request, 'my_web/index.html', {
        'token_valid': token_valid, 'token_re': token_re,
        'search_template': search_example_get, 'add_': add_,
        'r_type': r_type,
    })


@require_GET
def namaz(request):
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
    return render(request, 'my_web/namaz.html', {
        'token_valid': token_valid, 'token_re': token_re,
    })


@require_GET
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

    # get quote
    add_ = rand_fact_or_quote(True)

    logger.info(f'function index: request {request}')
    return render(request, 'my_web/news-feed.html', {
        'token_valid': token_valid, 'token_re': token_re,
        'loading_button_text': loading_button_text,
        'add_': add_,
    })


@require_GET
def tiktok(request):
    """
    TikTok page view
    :param request: request body
    :return: render template page
    """
    if settings.TIKTOK_PAGE_ENABLED:
        # unix time mark encryption
        salt = Fernet(load_more_encrypt_key)
        data = str.encode(str(round(time())))
        token_valid = salt.encrypt(data).decode("utf-8")
        token_re = settings.RETOKEN_PUBLIC

        # get quote
        add_ = rand_fact_or_quote(True)

        logger.info(f'function index: request {request}')
        return render(request, 'my_web/tiktok.html', {
            'token_valid': token_valid, 'token_re': token_re,
            'loading_button_text': loading_button_text,
            'add_': add_
        })

    return error_404(request)


@require_GET
def status(request):
    """
    Status page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function index: request {request}')
    status_data = status_data_api()
    return render(request, 'my_web/status.html', {'status': status_data})


@require_GET
def info(request):
    """
    Info site page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function info: request {request}')
    return render(request, 'my_web/info.html')


@require_GET
def botpage(request):
    """
    Bot info page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function index: request {request}')
    return render(request, 'my_web/botpage.html', )


@require_GET
def awareview(request, awareid):
    """
    Aware page view
    :param awareid: searching fact id
    :param request: request body
    :return: render template page
    """
    logger.info(f'function awareview: request {request}; awareid {awareid}')
    try:
        awareid: request.GET.get('awareid', '')
        aware_data = AWARE_Page.objects.get(unique_id=awareid)
        return render(request, 'my_web/awareview.html', {
            'aware': aware_data,
        })
    except Exception as e:
        logger.error(e)
        return error_404(request, str(e))


@require_POST
@cache_page(60 * 180)
def load_more(request):
    """
    Technical (load_more) page view
    :param request: request body
    :return: render template page
    """
    try:
        token = request.POST.get('validtoken', '')
        typeload = request.POST.get('typeload', '')
        r_token = request.POST.get('gr_token', '')
    except Exception as e:
        token = typeload = r_token = 0
        logging.error(e)

    if recaptcha_get_result(r_token):

        additions = int(request.POST.get('additions', ''))
        news_append = int(request.POST.get('news', ''))
        covid_stat_append = int(request.POST.get('covid_stat', ''))
        search = request.POST.get('search', '')
        search_index = request.POST.get('search_index_', '')
        namaz = request.POST.get('namaz', '')
        mobile = request.POST.get('mobile', '')
        videos = request.POST.get('videos', '')

        if not videos:
            # If the variable does not exist, then set its value - 0
            videos = 0

        user_address = request.headers['X-Forwarded-For'].replace(' ', '').split(',')[0]
        user_agent = request.headers['User-Agent']
        user_request_method = request.method

        try:
            user_referer = request.headers['HTTP_REFERER']
        except Exception as e:
            logger.warning(e)
            user_referer = 'no'

        if not search_index:
            search_index = 0
        else:
            search_index = int(search_index)

        if namaz:
            namaz = get_namaz_data(search)

        if videos:
            videos = tiktok_data_get()

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
                news = newsfeed(news_append)

                # image proxy encrypt data
                salt = Fernet(image_proxy_key)
                data = str.encode(str(round(time())))
                token_valid = salt.encrypt(data).decode("utf-8")

                # calculator
                c_result, c_input = calculator(search)

                # news link append
                news_link_add = news_search_in_str(search)

                # Send data to InfoBot
                if search:
                    if namaz:
                        search_type_data = 'namaz'
                    else:
                        search_type_data = 'search request'

                    Process(
                        target=infobot_send_data,
                        args=(
                            user_agent,
                            user_address,
                            search,
                            search_type_data,
                            user_request_method,
                            user_referer,
                        )
                    ).start()

                # Search API
                search_api = search_execute(search, search_index)
                search_data = search_api['data']
                search_array = search_api['array']

                # DeepL API
                translate_result = translate_simple(search)

                # data pack
                data = zip(news, search_array)

                logger.info(f'function load_more: request {request}')

                return render(request, 'my_web/load_more.html', {
                    'data': data, 'token_image_proxy': token_valid,
                    'typeload': typeload, 'covid_ru': covid_stat_ru,
                    'covid_ua': covid_stat_ua, 'additions': additions,
                    'news_append': news_append, 'covid_stat_append': covid_stat_append,
                    'c_result': c_result, 'search': search, 'c_input': c_input,
                    'news_search_in_str': news_link_add, 'search_data': search_data,
                    'namaz_data': namaz, 'videos': videos, 'user_address_original': user_address,
                    'translate_result': translate_result, 'mobile': mobile,
                })

    return error_400(request)


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def search_config(request):
    """
    Search XML config
    :param request: request body
    :return: render template page
    """
    return render(request, 'my_web/search.xml', content_type='text/xml')


def error_400(request, exception='Unknown'):
    """
    400 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    return JsonResponse({
        'code': 400,
        'description': 'Bad Request',
    }, status=400)


def error_403(request, exception='Unknown'):
    """
    403 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    logger.warning(str(exception)[:150] + '...')
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 403. Отказано в доступе.'}, status=403)


def error_404(request, exception='Unknown'):
    """
    404 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    logger.warning(str(exception)[:150] + '...')
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, status=404)


def error_500(request, exception='Unknown'):
    """
    500 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    logger.warning(str(exception)[:150] + '...')
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 500. Внутренняя ошибка сервера.'}, status=500)
