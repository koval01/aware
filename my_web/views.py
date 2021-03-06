from django.template.defaulttags import register
from django.http import HttpResponseForbidden
from django.shortcuts import render
from random import randrange, randint, choice
from .models import Post, Quote, Facts, Info, Statistic
from .newsapi import __main__ as newsfeed
from .porfirevich.api import __main__ as porfirevich_strory
from .porfirevich.api import get_story as get_story_porfirevich
import logging, string


@register.filter
def get_range(value):
    """
    Random range value generator functiontion
    :param value: Input max value
    :return: Output random range value
    """
    logging.info(f'function get_range: val {value}')
    return randrange(1, value)


@register.filter
def get_randint(value):
    """
    Random integer function
    :param value: Input max random value
    :return: Random value result
    """
    logging.info(f'function get_randint: val {value}')
    return randint(1, value)


@register.filter
def get_range_list(value):
    """
    Set range value function
    :param value: Some value set
    :return: Output result
    """
    logging.info(f'function get_range_list: val {value}')
    return range(value)


@register.filter
def cut_text(string):
    """
    String cut function (256 symbols)
    :param string: String for cut
    :return: Cut string result
    """
    logging.info(f'function cut_text: string {string}')
    return string[:256]+'...'


@register.filter
def get_item(item):
    """
    Print data from template function
    :param item: Input data
    :return: return print data
    """
    logging.info(f'function get_item: string {item}')
    return print(item)


@register.filter
def get_random_string(length = 16):
    """
    Random string generator function
    :param length: length string
    :return: generated string
    """
    letters = string.ascii_letters + string.digits
    result_str = ''.join(choice(letters) for i in range(length))
    return result_str


def index(request):
    """
    Index page view
    :param request: request body
    :return: render template page
    """
    logging.info(f'function index: request {request}')
    return render(request, 'my_web/index.html', )


def status(request):
    """
    Status page view
    :param request: request body
    :return: render template page
    """
    logging.info(f'function index: request {request}')
    return render(request, 'my_web/status.html', )


def botpage(request):
    """
    Bot info page view
    :param request: request body
    :return: render template page
    """
    logging.info(f'function index: request {request}')
    return render(request, 'my_web/botpage.html', )


def info(request):
    """
    Info site page view
    :param request: request body
    :return: render template page
    """
    logging.info(f'function info: request {request}')
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
    logging.info(f'function postview: request {request}; postid {postid}')
    try:
        postid: request.GET.get('postid', '')
        for p in Post.objects.raw('SELECT * FROM my_web_post WHERE id = {} LIMIT 1'.format(postid)):
            post = p
        posttitle = str(post.user_text + post.bot_text)
        if len(posttitle) > 64:
            posttitle = posttitle[:64] + '...'
        return render(request, 'my_web/postview.html', {'postget': post, 'posttitle': posttitle}, )
    except Exception as e:
        logging.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def storyview(request, storyid):
    """
    Story page view
    :param storyid: searching story id
    :param request: request body
    :return: render template page
    """
    logging.info(f'function storyview: request {request}; storyid {storyid}')
    try:
        storyid: request.GET.get('storyid', '')
        if not get_story_porfirevich(storyid):
            return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )

        text, time, likes, id_s = get_story_porfirevich(storyid)
        title = text
        if len(text) > 64:
            title = title[:64] + '...'
        return render(request, 'my_web/storyview.html', {
            'text': text, 'title': title, 'time': time,
            'likes': likes, 'id_s': id_s
        })
    except Exception as e:
        logging.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def quoteview(request, quoteid):
    """
    Quote page view
    :param quoteid: searching quote id
    :param request: request body
    :return: render template page
    """
    logging.info(f'function quoteview: request {request}; quoteid {quoteid}')
    try:
        postid: request.GET.get('postid', '')
        for q in Quote.objects.raw('SELECT * FROM my_web_quote WHERE id = {} LIMIT 1'.format(quoteid)):
            quote = q
        quotetitle = str(quote.q_text)
        if len(quotetitle) > 64:
            quotetitle = quotetitle[:64] + '...'
        return render(request, 'my_web/quoteview.html', {'quoteget': quote, 'quotetitle': quotetitle})
    except Exception as e:
        logging.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'})


def factview(request, factid):
    """
    Fact page view
    :param factid: searching fact id
    :param request: request body
    :return: render template page
    """
    logging.info(f'function factview: request {request}; factid {factid}')
    try:
        factid: request.GET.get('factid', '')
        for f in Facts.objects.raw('SELECT * FROM my_web_facts WHERE id = {} LIMIT 1'.format(factid)):
            fact = f
        facttitle = str(fact.f_text)
        if len(facttitle) > 64:
            facttitle = facttitle[:64] + '...'
        return render(request, 'my_web/factview.html', {'factget': fact, 'facttitle': facttitle}, )
    except Exception as e:
        logging.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def infoview(request, infoid):
    """
    Info page view
    :param infoid: searching info id
    :param request: request body
    :return: render template page
    """
    logging.info(f'function infoview: request {request}; infoid {infoid}')
    try:
        infoid: request.GET.get('infoid', '')
        for i in Info.objects.raw('SELECT * FROM my_web_info WHERE id = {} LIMIT 1'.format(infoid)):
            info = i
        infotitle = str(info.i_title)
        if len(infotitle) > 128:
            infotitle = infotitle[:128] + '...'
        return render(request, 'my_web/infoview.html', {'infoget': info, 'infotitle': infotitle}, )
    except Exception as e:
        logging.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def stats(request):
    """
    Statistics page view
    :param request: request body
    :return: render template page
    """
    logging.info(f'function stats: request {request}')
    try:
        for s in Statistic.objects.raw('SELECT * FROM my_web_statistic LIMIT 1'):
            stat = s
        sumstat = str(int(stat.u_stat) + int(stat.b_stat))
        return render(request, 'my_web/stats.html', {'statget': stat, 'sumstat': sumstat}, )
    except Exception as e:
        logging.error(e)
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def load_more(request):
    """
    Technical (load_more) page view
    :param request: request body
    :return: render template page
    """
    if request.POST:
        logging.info(f'function load_more: request {request}')
        stories = porfirevich_strory()
        posts = Post.objects.order_by('?')[:20]
        quotes = Quote.objects.order_by('?')[:20]
        facts = Facts.objects.order_by('?')[:20]
        news = newsfeed()
        data = zip(stories, posts, quotes, facts, news)
        return render(request, 'my_web/load_more.html', {'data': data})
    else:
        return HttpResponseForbidden()


def error_400(request, exception):
    """
    400 error handler page view
    :param request: request body
    :return: render template page
    """
    logging.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 400. Плохой запрос.'}, )


def error_403(request, exception):
    """
    403 error handler page view
    :param request: request body
    :return: render template page
    """
    logging.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 403. Отказано в доступе.'}, )


def error_404(request, exception):
    """
    404 error handler page view
    :param request: request body
    :return: render template page
    """
    logging.warning(exception)
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )
