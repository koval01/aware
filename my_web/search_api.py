from requests import get
from json import loads
from .covid.config import USER_AGENT
from django.conf import settings
from random import shuffle
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


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
                "safe": 1,
                "start": index,
            }
            r = get(u, headers=headers, params=params)
            if r.status_code != 200:
                logger.error("%s (LEN:%s) %s %s" % (keys[i], len(keys), r.status_code, loads(r.text)['error']['message']))
            else:
                return loads(r.text)
        except Exception as e:
            logger.error(e)


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

                array.append(dict(
                    title=i['title'],
                    link=i['link'],
                    displayLink=i['displayLink'],
                    snippet=snippet,
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