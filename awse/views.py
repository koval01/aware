import logging
import os
import random
from datetime import timedelta, datetime
from random import randint, choice
from time import time

import pafy
from blacklist.ratelimit import blacklist_ratelimited
from cryptography.fernet import Fernet
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from ratelimit.decorators import ratelimit
from requests import get

from .other.common_functions import check_bot_request_search, check_request__
from .other.common_functions import get_random_string as rand_str
from .other.heroku_api import get_last_build_id as heroku_get_last_build_id
from .other.quote_get import get_result as get_quote_list
from .search_utils.calculate import calculator
from .search_utils.namaz_api import get_namaz_data
from .search_utils.search_api import select_type as search_execute
from .search_utils.search_complete_api import get_result_data as search_complete
from .search_utils.weather_api import weather_get, get_weather_icon
from .other.whois_api import get_info_domain
from .covid.api import covid_api as covid_stat
from .covid.api import num_formatter
from .models import Info, Banner
from .news_rev.newsapi import __main__ as newsfeed
from .news_rev.newsapi_ai import __main__ as newsapiai_get
from .news_rev.twitterget import __main__ as twitter_news
from .other.text_encoder import encode as encoder_eng

logger = logging.getLogger(__name__)
image_proxy_key = settings.IMAGE_PROXY_KEY
img_link_proxy_key = settings.IMAGE_PROXY_LINK_KEY
load_encrypt_key = settings.LOAD_ENCRYPT_KEY
ad_key = settings.ADVERTISE_BOT_KEY
bot_check_tk = settings.BOT_CHECK_TOKEN
sign_key = settings.SIGN_ENCRYPT_KEY
qwriter_api_for_awse = os.environ['AWSE_KEY']
max_search_len = settings.MAX_SEARCH_LENGTH


@register.filter
def get_weather_ico(value) -> str:
    return get_weather_icon(value)


@register.filter
def encode_eng(value) -> str:
    return encoder_eng(value)


@register.filter
def add_days_by_timestamp(value=1) -> object:
    s = (value * 86400) + round(time())
    return datetime.fromtimestamp(s)


@register.filter
def pop_convert_weather(value) -> str:
    return str(value)[-2:] + '%'


@register.filter
def cut_long_words(string) -> str:
    return ' '.join([i[:32] for i in string.split()])


@register.filter
def seconds_to_time(val) -> str:
    return str(timedelta(seconds=val))


@register.filter
def get_random_string(length=16) -> str:
    return rand_str(length)


@register.filter
def link_encrypt_img(link) -> str:
    try:
        salt_link = Fernet(img_link_proxy_key)
        data_link = str.encode(str(link))
        result = salt_link.encrypt(data_link).decode("utf-8")

        return result

    except Exception as e:
        logger.error("%s: %s" % (link_encrypt_img.__name__, e))


@register.filter
def num_rounder_custom(val) -> str:
    return num_formatter(val)


@register.filter
def sign_address_encrypt(address) -> str:
    try:
        salt_sign = Fernet(sign_key)
        data_sign = str.encode(str(address))
        result = salt_sign.encrypt(data_sign).decode("utf-8")
        return result

    except Exception as e:
        logger.error("%s: %s" % (sign_address_encrypt.__name__, e))


def my_ip_key(group, request):
    try:
        if settings.CLOUDFLARE:
            user_address = request.headers['CF-Connecting-IP']

        else:
            head = request.headers['X-Forwarded-For']
            user_address = (head.split(',')[-1:][0]).strip()


    except Exception as e:
        user_address = '127.0.0.1'
        logger.error("%s: %s" % (my_ip_key.__name__, e))

    try:
        namaz = request.POST.get('namaz', '')

    except Exception as e:
        namaz = None
        logger.error(e)

    if namaz:
        user_address = '.'.join([str(random.randint(0, 255)) for _ in range(4)])

    return user_address


@require_GET
@ratelimit(key=my_ip_key, rate='30/s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def image_proxy_view(request):
    """
    Image proxy function
    :param request: body request
    :return: raw image
    """
    try:
        salt = Fernet(sign_key)
        received_address = salt.decrypt(str.encode(str(request.GET['sign']))).decode('utf-8')
        original_address = my_ip_key(None, request)

        logger.debug('%s: check address...' % image_proxy_view.__name__)

        if original_address == received_address:
            url = request.GET['data']
            salt_link = Fernet(img_link_proxy_key)
            link_get = salt_link.decrypt(str.encode(str(url))).decode('utf-8')

            logger.debug('%s: check image link...' % image_proxy_view.__name__)

            token = request.GET['token']
            salt = Fernet(image_proxy_key)
            token_get = int(salt.decrypt(str.encode(str(token))).decode('utf-8')) + 25
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
        logger.error("%s: %s" % (image_proxy_view.__name__, e))

    return error_400(request)


@require_GET
@cache_page(60 * 180)
@ratelimit(key=my_ip_key, rate='10/s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def search_suggestions_get(request):
    """
    We receive search suggestions
    :param request: request body
    :return: list suggestions
    """
    try:
        q = request.GET['q']
        if q and len(q) <= 100:
            return JsonResponse({"data": search_complete(q)})

    except Exception as e:
        logger.warning("%s: %s" % (search_suggestions_get.__name__, e))

    return error_400(request)


@require_GET
@ratelimit(key=my_ip_key, rate='10/s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def sync_time_server(request):
    return JsonResponse({"time_unix": round(time())})


@require_POST
@ratelimit(key=my_ip_key, rate='10/s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
@cache_page(60 * 240)
def whois_data(request):
    domain = request.POST.get('name', '')
    token = request.POST.get('token', '')
    if check_request__(token):
        return JsonResponse(get_info_domain(domain))
    return error_400(request)


def global_ad_function(lang: str) -> dict:
    """
    Global feature for getting advertising inside viws.py
    :param lang: Language (language code)
    :return: Dictionary with data
    """
    valid_codes_lang = ['ua', 'ru', 'en']

    if not lang or lang not in valid_codes_lang:
        lang = "ru"

    obj = Info.objects
    all_data = obj.all().filter(i_language=lang, i_active='yes')

    if all_data.count():
        logger.debug("%s: data count - %d" % (global_ad_function.__name__, all_data.count()))

        max_retry = round(200 / (obj.count() / 4))
        done_get = False
        n = 0

        while max_retry >= n:
            n += 1  # Add cycle to counter
            if not done_get and obj.exists():
                for i in all_data:
                    if i.i_chance >= randint(1, 100):
                        if randint(1, 6) > randint(1, 6) \
                                and round(time()) < round(i.i_time_active.timestamp()):
                            done_get = True
                            obj.filter(id=i.id).update(i_views=i.i_views + 1)  # Add one view

                            return i


@require_POST
@csrf_exempt
@ratelimit(key=my_ip_key, rate='3/s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def get_ad(request):
    """
    Get advertise
    :param request: request body
    :return: advertise data
    """
    try:
        key = request.POST.get('c_t___kk_', '')
        if key == ad_key or check_request__(key):
            lang = request.POST.get('lang', '')

            try:
                index_block_mode = request.GET['index_block_mode']

            except Exception as e:
                index_block_mode = False
                logger.warning("%s: %s" % (get_ad.__name__, e))

            finally:
                logger.info("Ad check...")
                data = global_ad_function(lang)

                if not data:
                    return JsonResponse({"error": "no ads available"})

                return JsonResponse({"text": data.i_text})

    except Exception as e:
        logger.error("%s: %s" % (get_ad.__name__, e))

    return error_400(request)


def global_banner_function() -> dict:
    """
    Global function for getting banners inside viws.py
    :return: Dictionary with data
    """
    obj = Banner.objects
    all_data = obj.all().filter(active='yes')

    if all_data.count():
        logger.debug("%s: data count - %d" % (global_banner_function.__name__, all_data.count()))

        max_retry = round(200 / (obj.count() / 4))
        if max_retry < 1:
            max_retry = 1
        done_get = False
        n = 0

        while max_retry >= n:
            n += 1  # Add cycle to counter
            if not done_get and obj.exists():
                for i in all_data:
                    if i.chance >= randint(1, 100):
                        if randint(1, 6) > randint(1, 6) \
                                and round(time()) < round(i.time_active.timestamp()):
                            done_get = True
                            obj.filter(id=i.id).update(views=i.views + 1)  # Add one view

                            return i


@require_POST
@ratelimit(key=my_ip_key, rate='3/s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def get_banner(request):
    """
    Get banner ad
    :param request: request body
    :return: video direct link
    """
    try:
        s = time()
        key = request.POST.get('c_t___kk_', '')

        if check_request__(key):
            data = global_banner_function()

            if not data:
                return JsonResponse({"error": "no ads available"})

            link = "https://%s/?utm_source=%s&utm_medium=%s&utm_campaign=%s&utm_content=%s&utm_term=%s" % (
                data.link_site,
                data.utm_source,
                data.utm_medium,
                data.utm_campaign,
                data.utm_content,
                data.utm_term,
            )

            img_link = link_encrypt_img(data.link_image)

            return JsonResponse({
                "link": img_link,
                "ad_site": link,
                "title": data.text,
                "id": "%s__%s" % (data.id, rand_str(32)),
                "time": str(time() - s)[:5]
            })

    except Exception as e:
        logger.error("%s: %s" % (get_banner.__name__, e))

    return error_400(request)


@require_POST
@ratelimit(key=my_ip_key, rate='2/s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def get_video_yt(request):
    """
    Get video from YouTube
    :param request: request body
    :return: video direct link
    """
    try:
        s = time()
        key = request.POST.get('c_t___kk_', '')
        video_id = request.POST.get('video_id', '')

        if check_request__(key):
            v = pafy.new(video_id)
            link = v.streams[0].url_https

            return JsonResponse({
                "link": link,
                "time": str(time() - s)[:5]
            })

    except Exception as e:
        logger.error("%s: %s" % (get_video_yt.__name__, e))

    return error_400(request)


@require_GET
@ratelimit(key=my_ip_key, rate='2/s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def index(request):
    """
    Index page view
    :param request: request body
    :return: render template page
    """
    # unix time mark encryption
    salt = Fernet(load_encrypt_key)
    data = str.encode(str(round(time())))
    token_valid = salt.encrypt(data).decode("utf-8")
    token_re = settings.RETOKEN_PUBLIC

    search_example_get = "What do you need to find?"

    user_address = my_ip_key(None, request)

    try:
        search_q = request.GET['q']

    except Exception as e:
        search_q = None
        logger.debug("%s: %s" % (index.__name__, e))

    logger.debug('%s: request - %s' % (index.__name__, request))

    return render(request, 'awse/index.html', {
        'token_valid': token_valid, 'token_re': token_re,
        'search_template': search_example_get,
        'search_q': search_q, 'user_address': user_address,
        'max_search_len': max_search_len
    })


@require_POST
@cache_page(60 * 180)
@ratelimit(key=my_ip_key, rate='1/3s', block=True)
@blacklist_ratelimited(timedelta(minutes=1))
def load(request):
    """
    Technical (load) page view
    :param request: request body
    :return: render template page
    """
    c_token = request.POST.get('c_t___kk_', '')
    sign_data = request.POST.get('sign', '')

    try:
        token = request.POST.get('validtoken', '')
        typeload = request.POST.get('typeload', '')

    except Exception as e:
        token = typeload = 0
        logging.error("%s: %s" % (load.__name__, e))

    salt = Fernet(sign_key)
    received_address = salt.decrypt(str.encode(sign_data)).decode('utf-8')
    original_address = my_ip_key(None, request)

    if check_request__(c_token) and original_address == received_address:
        additions = int(request.POST.get('additions', ''))
        news_append = int(request.POST.get('news', ''))
        covid_stat_append = int(request.POST.get('covid_stat', ''))
        search = request.POST.get('search', '')
        len_c = request.POST.get('c', '')
        search_index = request.POST.get('search_index_', '')
        namaz = request.POST.get('namaz', '')
        mobile = request.POST.get('mobile', '')
        quote_mode = request.POST.get('quote_mode', '')

        news_need_load = request.POST.get('news_need', '')
        weather_need_load = request.POST.get('weather_need', '')

        if int(quote_mode):
            quote = choice(get_quote_list())
        else:
            quote = None

        logger.debug('%s: Parameters parsed.' % load.__name__)

        try:
            last_time_key = int(request.POST.get('l', ''))
        except Exception as e:
            last_time_key = 9999999 * 9999999
            logger.debug(e)

        if len(search) <= max_search_len:
            logger.debug('%s: Check search length and continue.' % load.__name__)

            user_address = original_address

            if not search_index:
                search_index = 0
            else:
                search_index = int(search_index)

            if namaz:
                namaz = get_namaz_data(search)

            if token and typeload and len(search) == int(len_c):
                logger.debug('%s: Check token and continue.' % load.__name__)

                if typeload == 'newsession' and covid_stat_append:
                    covid_stat_ua = covid_stat('UA')
                    covid_stat_ru = covid_stat('RU')
                else:
                    covid_stat_ua = 0
                    covid_stat_ru = 0

                # token decrypt
                try:
                    salt = Fernet(load_encrypt_key)
                    token_get = int(salt.decrypt(str.encode(str(token))).decode('utf-8'))
                except Exception as e:
                    token_get = 0
                    logging.error(e)

                if token_get and (token_get + 72000) > round(time()):
                    logger.debug('%s: Check "token_get" and continue.' % load.__name__)

                    # data collect
                    # news = newsfeed(news_append)

                    # image proxy encrypt data
                    salt = Fernet(image_proxy_key)
                    data = str.encode(str(round(time())))
                    token_valid = salt.encrypt(data).decode("utf-8")

                    # calculator
                    c_result, c_input = calculator(search)

                    # Search API
                    search_send = search
                    if namaz:
                        search_send = ''

                    # default search
                    search_api = search_execute(search_send, search_index)
                    search_data = search_api['data']
                    search_array = search_api['array']

                    # image search
                    if settings.IMAGES_SEARCH_ENABLED:
                        images_search = search_execute(search_send, 0, 'image')['items']
                    else:
                        images_search = None

                    # Weather
                    if weather_need_load:
                        weather = weather_get(search)
                    else:
                        weather = {}

                    # DeepL API
                    # translate_result = translate_simple(search)
                    translate_result = None

                    # data pack
                    data = zip(search_array)  # only search data remains

                    # news data load
                    country = settings.AVAILABLE_COUNTRY[0]

                    if news_need_load:
                        tweets = twitter_news(country)
                        ai_news = newsapiai_get(country)
                        news_ = newsfeed(country)

                        news_data_list = sorted(
                            [el for el in (ai_news + news_ + tweets) if el['time'] < last_time_key],
                            key=lambda x: x['time'], reverse=True
                        )[:50]
                    else:
                        news_data_list = []

                    # all variables
                    class Variables:
                        def __init__(self):
                            self.token_image_proxy = token_valid
                            self.images_search = images_search

                            self.mobile = mobile
                            self.user_address_original = user_address

                            self.search_index = search_index
                            self.typeload = typeload

                            self.covid_ru = covid_stat_ru
                            self.covid_ua = covid_stat_ua

                            self.additions = additions
                            self.news_data_list = news_data_list
                            self.news_append = news_append
                            self.covid_stat_append = covid_stat_append

                            self.c_result = c_result
                            self.c_input = c_input

                            self.search = search
                            self.search_data = search_data

                            self.namaz_data = namaz
                            self.quote = quote

                            self.translate_result = translate_result
                            self.weather = weather
                            self.search_api_full_dict = search_api

                            # other
                            self.check_bot_request_search = check_bot_request_search(search)
                            self.settings = settings

                    vars_ = vars(Variables())

                    logger.debug('%s: request - %s' % (load.__name__, request))

                    return render(request, 'awse/load.html', {
                        'data': data, 'vars': vars_,
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
def footer_html(request):
    lines = [
        '<p style="color: #a5a5a5;font-size:13px;margin-bottom:-5%;text-align:center">',
        'Sponsored by <a href="https://t.me/Jomahmadov2002" style="color: #636363;">Jomahmadov Najibullo</a>',
        '</p><br/>',
        '<p style="color: #a5a5a5;font-size:13px;margin-bottom:-5%;text-align:center">',
        'Developed by <a href="https://t.me/koval_yaroslav" style="color: #636363;">Koval Yaroslav</a>',
        '</p><br/>',
        '<p style="color: #a5a5a5;font-size:13px;margin-bottom:-5%;text-align:center">',
        'Logo by <a href="https://t.me/SashkoTsomyk" style="color: #636363;">Ts\'omyk Sasha</a>',
        '</p><br/>',
        '<p class="build_info_footer" style="color:#525254;font-size:12px;margin-bottom:-5%;text-align:center">',
        'Build ID: awse-%s' % heroku_get_last_build_id(),
    ]
    return HttpResponse("".join(lines), content_type="text/html; charset=utf-8")


@require_GET
def search_config(request):
    """
    Search XML config
    :param request: request body
    :return: render template page
    """
    return render(request, 'awse/search.xml', content_type='text/xml')


def error_400(request, exception='Unknown'):
    """
    400 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    return render(request, 'awse/error.html', {
        'error_code': 400,
        'description': 'We cannot accept this request. I don\'t know why, we just can\'t..'
    }, status=400)


def error_403(request, exception='Unknown'):
    """
    403 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    return render(request, 'awse/error.html', {
        'error_code': 403,
        'description': 'We cannot accept this request. This page is restricted.'
    }, status=403)


def error_404(request, exception='Unknown'):
    """
    404 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    return render(request, 'awse/error.html', {
        'error_code': 404,
        'description': 'This page was not found on this server'
    }, status=404)


def error_500(request, exception='Unknown'):
    """
    500 error handler page view
    :param request: request body
    :param exception: exception request error
    :return: render template page
    """
    return render(request, 'awse/error.html', {
        'error_code': 500,
        'description': 'The server was unable to process this request. What did those programmers do there again...'
    }, status=500)
