from random import choice
from string import ascii_letters, digits
from requests import get
from datetime import datetime
from time import time
import difflib, re, logging, calendar

logger = logging.getLogger(__name__)


def get_random_string(length=16) -> str:
    """
    Random string generator function
    :param length: length string
    :return: generated string
    """
    return ''.join(choice(ascii_letters + digits + '_-') for i in range(length))


def similarity(string_one, string_two):
    matcher = difflib.SequenceMatcher(
        None, string_one.lower(), string_two.lower()
    )
    return matcher.ratio()


def check_bot_request_search(string) -> bool:
    """
    Перевірка чи пов'язаний запит з ботом
    :param string: Строка в якій виконується пошук
    :return: Результат перевірки
    """
    words_get = string.lower().split()
    words_list = [
        'бот', 'bot', 'телеграм', 'telegram', 'aware', 'поисковик', 'аваре',
        'авар', 'awar', 'телеграмм',
    ]
    for i in words_get:
        a = ''.join(filter(str.isalpha, i))
        for x in words_list:
            if similarity(a, x) > 0.80:
                return True


def check_info_request_search(string) -> bool:
    """
    Перевірка чи пов'язаний запит з інформацією (описом проекту)
    :param string: Строка в якій виконується пошук
    :return: Результат перевірки
    """
    words_get = string.lower().split()
    words_list = [
        'awse', 'aware', 'авар', 'аваре', 'awse.us', 'эвси', 'авси'
    ]
    for i in words_get:
        a = ''.join(filter(str.isalpha, i))
        for x in words_list:
            if similarity(a, x) > 0.80:
                return True


def check_link(link) -> str:
    """
    Перевірка чи є переадресації в посиланні
    :param link: Посилання для перевірки
    :return: Отримане посилання
    """
    return get(link, timeout=1).url


def num_formatter(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return ('%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])).replace('.00', '')


def check_request__(data) -> bool:
    """
    Перевірка запиту
    :param data: Отримана інформація (str)
    :return: bool result
    """
    try:
        s = re.findall(r'[_].*?[_]', data)
        x = re.sub(r'\D', '', s[0])[:10]
        y = re.sub(r'\D', '', s[1])[:10]

        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())

        if int(x)+8 > round(unixtime) and int(y)+12 > round(time()):
            # check user UTC time and server time
            return True
    except Exception as e:
        logger.error(e)