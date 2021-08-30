import logging
import requests_cache

from django.conf import settings

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession(backend='memory', cache_name='quote_get_cache')


def get_result() -> dict:
    """
    Get random quotes list
    :return: response dict
    """
    try:
        headers = {
            "User-Agent": settings.REQ_USER_AGENT,
        }
        r = session.get("https://zenquotes.io/api/quotes", headers=headers)
        if r.status_code == 200:
            return r.json()

    except Exception as e:
        logger.error(e)
