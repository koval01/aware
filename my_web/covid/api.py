from bs4 import BeautifulSoup
from .config import USER_AGENT, API_URL, API_URL_RU
import logging, re, requests_cache

session = requests_cache.CachedSession('covid_cache', expire_after=7200)
logger = logging.getLogger(__name__)

def num_formatter(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def __main__(country='UA') -> str:
    error_http = False;
    error_parse = False;
    error_decode = False
    headers = {"user-agent": USER_AGENT}
    array = []

    if country == 'UA':
        try:
            http_response = session.get(API_URL, headers=headers)
        except Exception as e:
            logger.error(e)
            error_http: True

        if not error_http:
            try:
                soup = BeautifulSoup(http_response.text, "html.parser")
                fields_all = soup.find_all('div', {"class": "one-field", "class": "info-count"})
            except Exception as e:
                logging.error(e)
                error_parse: True

            for i in fields_all:
                try:
                    soup_local = BeautifulSoup(str(i), "html.parser")
                    array.append(soup_local.find('div', {"class": "field-value"}).text.replace('\n', '').replace('\t', ''))
                except Exception as e:
                    logging.error(e)
                    error_decode: True

            def ukr_month_to_russian(string) -> str:
                """local function mont translate"""
                ua_month = ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня',
                            'вересня', 'жовтня', 'листопада', 'грудня']
                ru_month = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                            'октября', 'ноября', 'декабря']
                for i, e in enumerate(ua_month):
                    if e in string:
                        return string.replace(e, ru_month[i])

            date = soup.find('span', {'style': 'color: #999999;'}).text
            date = ukr_month_to_russian(date)
            array.append(date.replace(
                'Інформація станом на', 'По состоянию на'
            ))

            if len(array) != 6:
                error_decode: True

        if error_http or error_parse or error_decode:
            logging.error(f'Error http: {error_http}; Error parsing: {error_parse}; Error decode: {error_decode};')
            return 0

    elif country == 'RU':
        try:
            http_response = session.get(API_URL_RU, headers=headers)
        except Exception as e:
            logger.error(e)
            error_http: True

        if not error_http:
            try:
                soup = BeautifulSoup(http_response.text, "html.parser")
                fields_all = soup.find_all('div', {"class": "cv-countdown__item"})
            except Exception as e:
                logging.error(e)
                error_parse: True

            for x, i in enumerate(fields_all):
                try:
                    soup_local = BeautifulSoup(str(i), "html.parser")
                    x = soup_local.find('div', {"class": "cv-countdown__item-value"}).text
                    x = x.replace('>', '').replace(' млн', '000000').replace(' ', '')
                    if x != 2:
                        x = num_formatter(int(x))
                    array.append(x)
                except Exception as e:
                    logging.error(e)
                    error_decode: True

            date = soup.find('div', {'class': 'cv-banner__description'}).text
            x_d = 'По состоянию на '
            date = x_d + date.replace(x_d, '').lstrip('0')
            array.append(re.sub(r'\d\d[:]\d\d', '', date))

            if len(array) != 6:
                error_decode: True

        if error_http or error_parse or error_decode:
            logging.error(f'Error http: {error_http}; Error parsing: {error_parse}; Error decode: {error_decode};')
            return 0

    return array


def covid_api(country) -> str:
    """
    Функція для виклику Covid Info API
    :return: Строка з даними
    """
    return __main__(country)