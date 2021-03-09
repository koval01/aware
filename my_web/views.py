from django.template.defaulttags import register
from django.http import HttpResponseForbidden, StreamingHttpResponse, Http404
from django.shortcuts import render
from random import randrange, randint, choice
from .models import Post, Quote, Facts, Info, Statistic
from .newsapi import __main__ as newsfeed
from .porfirevich.api import __main__ as porfirevich_strory
from .porfirevich.api import get_story as get_story_porfirevich
from .porfirevich.api import cleanhtml
from .link_analyze import link_image as img_link_check
from cryptography.fernet import Fernet
from time import time
import logging, string, requests, os


logger = logging.getLogger(__name__)

image_proxy_key = os.environ['IMAGE_PROXY_KEY']
image_link_key = os.environ['IMAGE_LINK_KEY']


@register.filter
def get_range(value) -> int:
    """
    Random range value generator functiontion
    :param value: Input max value
    :return: Output random range value
    """
    logger.info(f'function get_range: val {value}')
    return randrange(1, value)


@register.filter
def get_randint(value) -> int:
    """
    Random integer function
    :param value: Input max random value
    :return: Random value result
    """
    logger.info(f'function get_randint: val {value}')
    return randint(1, value)


@register.filter
def get_range_list(value) -> range:
    """
    Set range value function
    :param value: Some value set
    :return: Output result
    """
    logger.info(f'function get_range_list: val {value}')
    return range(value)


@register.filter
def cut_text(string) -> str:
    """
    String cut function (256 symbols)
    :param string: String for cut
    :return: Cut string result
    """
    logger.info(f'function cut_text: string {string}')
    return string[:256]+'...'


@register.filter
def get_item(item) -> print:
    """
    Print data from template function
    :param item: Input data
    :return: return print data
    """
    logger.info(f'function get_item: string {item}')
    return print(item)


@register.filter
def get_random_string(length=16) -> str:
    """
    Random string generator function
    :param length: length string
    :return: generated string
    """
    letters = string.ascii_letters + string.digits + '_-'
    return ''.join(choice(letters) for i in range(length))


@register.filter
def get_id(l) -> str:
    """
    Get id block
    :param len: set len or random if len = 0
    :return: generated id
    """
    if l: l = len
    else: l = randint(16, 24)
    return get_random_string(randint(12, l))


@register.filter
def link_encrypt_img(link) -> str:
    """
    Link encryptor
    :param link: Link image
    :return: Encrypted link
    """
    salt_link = Fernet(img_link_proxy_key)
    data_link = str.encode(str(link))
    return salt_link.encrypt(data_link).decode("utf-8")


def image_proxy_view(request):
    if request.GET:
        try:
            url = request.GET['data']
            salt_link = Fernet(img_link_proxy_key)
            link_get = salt_link.decrypt(str.encode(str(url))).decode('utf-8')
            if img_link_check(link_get):
                token = request.GET['token']
                salt = Fernet(image_proxy_key)
                token_get = int(salt.decrypt(str.encode(str(token))).decode('utf-8')) + 10
                control_time = round(time())
                if token_get > control_time:
                    response = requests.get(
                        link_get, stream=True,
                        headers={'user-agent': request.headers.get('user-agent')}
                    )
                    return StreamingHttpResponse(
                        response.raw,
                        content_type=response.headers.get('content-type'),
                        status=response.status_code,
                        reason=response.reason)
        except Exception as e:
            logger.error(e)
    return HttpResponseForbidden()


def index(request):
    """
    Index page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function index: request {request}')
    return render(request, 'my_web/index.html', )


def status(request):
    """
    Status page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function index: request {request}')
    return render(request, 'my_web/status.html', )


def botpage(request):
    """
    Bot info page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function index: request {request}')
    return render(request, 'my_web/botpage.html', )


def info(request):
    """
    Info site page view
    :param request: request body
    :return: render template page
    """
    logger.info(f'function info: request {request}')
    info_pages = Info.objects.order_by('-id')[:50]
    return render(request, 'my_web/info.html', {'infoget': info_pages},)


def postview_(request):
    """
    Post not found page view
    :param request: request body
    :return: render template page
    """
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 400. Плохой запрос.'}, )


def storyview_(request):
    """
    Story not found page view
    :param request: request body
    :return: render template page
    """
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 400. Плохой запрос.'}, )


def quoteview_(request):
    """
    Quote not found page view
    :param request: request body
    :return: render template page
    """
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 400. Плохой запрос.'}, )


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
        for p in Post.objects.raw('SELECT * FROM my_web_post WHERE id = {} LIMIT 1'.format(postid)):
            post = p
        posttitle = str(post.user_text + post.bot_text)
        if len(posttitle) > 64:
            posttitle = posttitle[:64] + '...'
        return render(request, 'my_web/postview.html', {'postget': post, 'posttitle': posttitle}, )
    except Exception as e:
        logger.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


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
            return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )

        text, time, likes, id_s = get_story_porfirevich(storyid)
        t = cleanhtml(text)
        title = t;short_text = t
        if len(text) > 64:
            title = title[:64] + '...'
        if len(text) > 1000:
            short_text = short_text[:1000] + '...'
        return render(request, 'my_web/storyview.html', {
            'text': text, 'title': title, 'time': time,
            'likes': likes, 'id_s': id_s, 'short_text': short_text
        })
    except Exception as e:
        logger.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


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
        for q in Quote.objects.raw('SELECT * FROM my_web_quote WHERE id = {} LIMIT 1'.format(quoteid)):
            quote = q
        quotetitle = str(quote.q_text)
        if len(quotetitle) > 64:
            quotetitle = quotetitle[:64] + '...'
        return render(request, 'my_web/quoteview.html', {'quoteget': quote, 'quotetitle': quotetitle})
    except Exception as e:
        logger.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'})


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
        for f in Facts.objects.raw('SELECT * FROM my_web_facts WHERE id = {} LIMIT 1'.format(factid)):
            fact = f
        facttitle = str(fact.f_text)
        if len(facttitle) > 64:
            facttitle = facttitle[:64] + '...'
        return render(request, 'my_web/factview.html', {'factget': fact, 'facttitle': facttitle}, )
    except Exception as e:
        logger.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def infoview(request, infoid):
    """
    Info page view
    :param infoid: searching info id
    :param request: request body
    :return: render template page
    """
    logger.info(f'function infoview: request {request}; infoid {infoid}')
    try:
        infoid: request.GET.get('infoid', '')
        for i in Info.objects.raw('SELECT * FROM my_web_info WHERE id = {} LIMIT 1'.format(infoid)):
            info = i
        infotitle = str(info.i_title)
        if len(infotitle) > 128:
            infotitle = infotitle[:128] + '...'
        return render(request, 'my_web/infoview.html', {'infoget': info, 'infotitle': infotitle}, )
    except Exception as e:
        logger.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


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
        logger.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def load_more(request):
    """
    Technical (load_more) page view
    :param request: request body
    :return: render template page
    """
    if request.POST:
        logger.info(f'function load_more: request {request}')
        stories = porfirevich_strory()
        posts = Post.objects.order_by('?')[:20]
        quotes = Quote.objects.order_by('?')[:20]
        facts = Facts.objects.order_by('?')[:20]
        news = newsfeed()
        # image proxy encrypt data
        salt = Fernet(image_proxy_key)
        data = str.encode(str(round(time())))
        token_valid = salt.encrypt(data).decode("utf-8")
        data = zip(stories, posts, quotes, facts, news)
        return render(request, 'my_web/load_more.html', {
            'data': data, 'token_image_proxy': token_valid
        })
    else:
        return HttpResponseForbidden()


def error_400(request, exception):
    """
    400 error handler page view
    :param request: request body
    :return: render template page
    """
    logger.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 400. Плохой запрос.'}, )


def error_403(request, exception):
    """
    403 error handler page view
    :param request: request body
    :return: render template page
    """
    logger.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 403. Отказано в доступе.'}, )


def error_404(request, exception):
    """
    404 error handler page view
    :param request: request body
    :return: render template page
    """
    logger.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )
