from django.template.defaulttags import register
from django.http import HttpResponseForbidden
from django.shortcuts import render
from random import randrange, randint, choice
from .models import Post, Quote, Facts, Info, Statistic
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
def get_item(item):
    logger.info(f'func get_item: string {item}')
    return print(item)


@register.filter
def get_random_string(length = 16):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(choice(letters) for i in range(length))
    return result_str


def index(request):
    logger.info(f'func index: request {request}')
    return render(request, 'my_web/index.html', )


def status(request):
    logger.info(f'func index: request {request}')
    return render(request, 'my_web/status.html', )


def botpage(request):
    logger.info(f'func index: request {request}')
    return render(request, 'my_web/botpage.html', )


def info(request):
    logger.info(f'func info: request {request}')
    info_pages = Info.objects.order_by('-id')[:50]
    return render(request, 'my_web/info.html', {'infoget': info_pages},)


def postview_(request):
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 400. Плохой запрос.'}, )


def quoteview_(request):
    return render(request, 'my_web/error.html', {'exception': 'Ошибка 400. Плохой запрос.'}, )


def postview(request, postid):
    logger.info(f'func postview: request {request}; postid {postid}')
    try:
        postid: request.GET.get('postid', '')
        for p in Post.objects.raw('SELECT * FROM my_web_post WHERE id = {} LIMIT 1'.format(postid)):
            post = p
        posttitle = str(post.user_text + post.bot_text)
        if len(posttitle) > 64:
            posttitle = posttitle[:64] + '...'
        return render(request, 'my_web/postview.html', {'postget': post, 'posttitle': posttitle}, )
    except:
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def quoteview(request, quoteid):
    logger.info(f'func quoteview: request {request}; quoteid {quoteid}')
    try:
        postid: request.GET.get('postid', '')
        for q in Quote.objects.raw('SELECT * FROM my_web_quote WHERE id = {} LIMIT 1'.format(quoteid)):
            quote = q
        quotetitle = str(quote.q_text)
        if len(quotetitle) > 64:
            quotetitle = quotetitle[:64] + '...'
        return render(request, 'my_web/quoteview.html', {'quoteget': quote, 'quotetitle': quotetitle})
    except:
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'})


def factview(request, factid):
    logger.info(f'func factview: request {request}; factid {factid}')
    try:
        factid: request.GET.get('factid', '')
        for f in Facts.objects.raw('SELECT * FROM my_web_facts WHERE id = {} LIMIT 1'.format(factid)):
            fact = f
        facttitle = str(fact.f_text)
        if len(facttitle) > 64:
            facttitle = facttitle[:64] + '...'
        return render(request, 'my_web/factview.html', {'factget': fact, 'facttitle': facttitle}, )
    except:
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def infoview(request, infoid):
    logger.info(f'func infoview: request {request}; infoid {infoid}')
    try:
        infoid: request.GET.get('infoid', '')
        for i in Info.objects.raw('SELECT * FROM my_web_info WHERE id = {} LIMIT 1'.format(infoid)):
            info = i
        infotitle = str(info.i_title)
        if len(infotitle) > 128:
            infotitle = infotitle[:128] + '...'
        return render(request, 'my_web/infoview.html', {'infoget': info, 'infotitle': infotitle}, )
    except:
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def stats(request):
    logger.info(f'func stats: request {request}')
    try:
        for s in Statistic.objects.raw('SELECT * FROM my_web_statistic LIMIT 1'):
            stat = s
        sumstat = str(int(stat.u_stat) + int(stat.b_stat))
        return render(request, 'my_web/stats.html', {'statget': stat, 'sumstat': sumstat}, )
    except:
        return render(request, 'my_web/error.html', {'exception': 'Ошибка 404. Страница не найдена.'}, )


def load_more(request):
    if request.POST:
        logger.info(f'func load_more: request {request}')
        posts = Post.objects.order_by('?')[:15]
        quotes = Quote.objects.order_by('?')[:8]
        facts = Facts.objects.order_by('?')[:8]
        news = newsfeed()
        return render(request, 'my_web/load_more.html', {'posts': posts, 'quotes': quotes, 'facts': facts, 'news': news},)
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
