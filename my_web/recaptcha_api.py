from requests import post
from json import loads
from django.conf import settings
import logging, requests_cache


requests_cache.install_cache('requests_cache_db_recaptcha_api')
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
        result = loads(r)['success']
    except Exception as e:
        logger.error(e)
        result = False

    return result