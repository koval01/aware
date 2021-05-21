from json import loads
from .covid.config import USER_AGENT
from urllib.parse import urlparse, parse_qs
from django.conf import settings
from random import shuffle
from bs4 import BeautifulSoup
import logging, requests_cache, re

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession('search_api_cache', expire_after=259200)


def get_result(question, index=1) -> dict:
    """
    Get search data
    :param question: Search string
    :param index: search index element
    :return: response dict
    """
    u = settings.SEARCH_API_HOST
    keys = settings.SEARCH_API_KEYS.split()
    cx = settings.SEARCH_CX
    shuffle(keys)
    for i, e in enumerate(keys):
        try:
            headers = {
                "User-Agent": USER_AGENT,
            }
            params = {
                "key": keys[i],
                "cx": cx,
                "q": question,
                "queries": 10,
                "safe": 0,
                "start": index,
            }
            r = session.get(u, headers=headers, params=params)
            if r.status_code != 200:
                logger.error("%s (LEN:%s) %s %s" % (keys[i], len(keys), r.status_code, loads(r.text)['error']['message']))
            else:
                return loads(r.text)
        except Exception as e:
            logger.error(e)


def search_youtube(link) -> str:
    """
    Перевірка чи веде посилання на YouTube
    :return: ID відео або None, якщо не веде на YouTube
    """
    domains = [
        'youtube.com', 'youtu.be',
    ]
    url = urlparse(link)

    try:
        if re.search(domains[0], link):
            return parse_qs(url.query)['v'][0]

        elif re.search(domains[1], link):
            return url.path.replace('/', '')

    except Exception as e:
        logger.warning(e)


def data_prepare(data) -> dict:
    try:
        if data['searchInformation']['totalResults']:
            array = []
            s = data['searchInformation']
            s_info = dict(
                formattedSearchTime=s['formattedSearchTime'],
                formattedTotalResults=s['formattedTotalResults'],
            )
            for i in data['items']:
                try:
                    snippet = BeautifulSoup(
                        i['snippet'], 'lxml'
                    ).text
                except Exception as e:
                    snippet = '...'
                    logger.warning(e)

                try:
                    thumb = i['pagemap']['cse_thumbnail'][0]['src']
                except Exception as e:
                    thumb = None
                    logger.warning(e)

                split_snippet = str(snippet).split()
                array_done = []

                for x in split_snippet:
                    if len(x) > 27:
                        x = x[:27]+"..."
                    array_done.append(x)
                snippet = " ".join(array_done)

                array.append(dict(
                    title=i['title'],
                    link=i['link'],
                    displayLink=i['displayLink'],
                    snippet=snippet,
                    thumb=thumb,
                    youtube=search_youtube(i['link']),
                ))
            return dict(s_info=s_info, array=array)
    except Exception as e:
        logging.error(e)


def search(string) -> dict:
    """
    Функція пошуку
    :param string: Пошуковий запит
    :return: Список результатів
    """
    def search_error():
        return dict(
            data='',
            array=[['' for _ in range(6)] for y in range(100)]
        )

    try:
        if not string:
            return search_error()

        array = []
        for i in range(2):
            if i == 0:
                s = 1
            else:
                s = i * 10 + 1
            x = get_result(string, s)
            d = data_prepare(x)
            if i == 1:
                data = d['s_info']
            array = array + d['array']
        return dict(data=data, array=array)
    except Exception as e:
        logger.warning(e)
        return search_error()


def search_custom_index(string, index) -> dict:
    """
    Функція пошуку
    :param string: Пошуковий запит
    :param index: Пошуковий індекс
    :return: Список результатів
    """
    x = get_result(string, index)
    d = data_prepare(x)
    return dict(data=d['s_info'], array=d['array'])


def select_type(string, index) -> dict:
    """
    Функція для зручного вибору режиму
    :param string: Пошукова строка
    :param index: Індекс
    :return: результат пошуку
    """
    if index:
        return search_custom_index(string, index)
    return search(string)