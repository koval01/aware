from requests import get
from json import loads
import logging, requests_cache


requests_cache.install_cache('requests_cache_db_wikipedia_api')
logger = logging.getLogger(__name__)


def get_random_article_wikipedia() -> dict:
    """
    Отримуємо випадковий запис з Вікіпедії
    :return: Token check result
    """
    u = 'https://ru.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'random',
        'rnlimit': '1',
        'prop': 'info|extracts',
        'inprop': 'url',
    }
    try:
        r = get(u, params=params).text
        result = loads(r)['success']
    except Exception as e:
        logger.error(e)
        result = False

    return result