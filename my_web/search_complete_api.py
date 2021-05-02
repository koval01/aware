from requests import get
from .covid.config import USER_AGENT
from bs4 import BeautifulSoup
from .common_functions import get_random_string
import logging

logger = logging.getLogger(__name__)


def get_result(question) -> str:
    """
    Get search data
    :param question: Search string
    :return: response dict
    """
    for i in range(3):
        try:
            headers = {
                "User-Agent": USER_AGENT,
            }
            params = {
                "q": question,
                "cp": 5,
                "client": "gws-wiz",
                "xssi": "t",
                "gs_ri": "gws-wiz",
                "hl": "ru-RU",
            }
            r = get("https://www.google.com.ua/complete/search", headers=headers, params=params)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            logger.error(e)


def data_prepare(data) -> list:
    """
    Підготовка даних
    :param data: Вхідні дані
    :return: Вихідні дані
    """
    x = data.replace(")]}'", '')
    return eval(x)


def get_result_data(question) -> str:
    """
    Отримання фінального результату
    :param question: Пошукова стрічка
    :return: Результат в форматі строки
    """
    d = get_result(question)
    r = data_prepare(d)
    return ''.join(['<li id="%s" class="aware-recommendation-search-el">%s</li>' % (get_random_string(), BeautifulSoup(i[0], 'lxml').text.capitalize()) for i in r[0]])