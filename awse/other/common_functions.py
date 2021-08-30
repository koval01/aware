import calendar
import difflib
import logging
import re
from datetime import datetime
from random import choice
from string import ascii_letters, digits
from time import time

from requests import get

logger = logging.getLogger(__name__)


def get_random_string(length=16) -> str:
    """
    Random string generator function
    :param length: length string
    :return: generated string
    """
    return ''.join(choice(ascii_letters + digits + '_') for i in range(length))


def create_dict_by_string(text: str) -> dict:
    array = "{"

    for i, e in enumerate(text):
        el = "%d: \"%s\", " % (i, e)
        array += el

    array += " "
    array = array.replace(",  ", "}")

    return eval(array)


def similarity(string_one, string_two):
    matcher = difflib.SequenceMatcher(
        None, string_one.lower(), string_two.lower()
    )
    return matcher.ratio()


def check_bot_request_search(string) -> bool:
    """
    Check if the query is related to the bot
    :param string: The period in which the search is performed
    :return: The result of the inspection
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
    Checking whether the request is related to the information (project description)
    :param string: The period in which the search is performed
    :return: The result of the inspection
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
    Check for redirects in the link
    :param link: Link to check
    :return: Received link
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
    Check request
    :param data: Received information (str)
    :return: bool result
    """
    try:
        s = re.findall(r'[_].*?[_]', data)
        x = re.sub(r'\D', '', s[0])[:10]
        y = re.sub(r'\D', '', s[1])[:10]

        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())

        if int(x) + 8 > round(unixtime) and int(y) + 12 > round(time()):
            # check user UTC time and server time
            return True
    except Exception as e:
        logger.error(e)
