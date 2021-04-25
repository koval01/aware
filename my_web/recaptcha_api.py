from requests import post
from json import loads
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def get_result(token) -> bool:
    """
    Check recaptcha result
    :param token: Check token
    :return: Token check result
    """
    u = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': settings.RETOKEN_PRIVATE,
        'response': token,
    }
    try:
        r = post(u, data=data).text
        return loads(r)['success']
    except Exception as e:
        logger.error(e)