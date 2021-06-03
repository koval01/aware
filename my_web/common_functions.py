from random import choice
from string import ascii_letters, digits
import difflib


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