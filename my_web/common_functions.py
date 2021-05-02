from random import choice
from string import ascii_letters, digits


def get_random_string(length=16) -> str:
    """
    Random string generator function
    :param length: length string
    :return: generated string
    """
    letters = ascii_letters + digits + '_-'
    return ''.join(choice(letters) for i in range(length))


def get_mobile_bool(bool_mobile_getted) -> bool:
    """
    Revers mobile data
    :param bool_mobile_getted: bool data
    :return: reversed bool data
    """
    if not bool_mobile_getted:
        return True