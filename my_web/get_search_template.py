from requests import post
from json import loads
from .covid.config import USER_AGENT
import logging

logger = logging.getLogger(__name__)


def get_result() -> str:
    """
    Get search template
    :return: Russian search template text
    """
    u = 'https://randstuff.ru/question/generate/'
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "X-Requested-With": "XMLHttpRequest",
        }
        r = post(u, headers=headers, timeout=3).text
        return loads(r)['question']['text']
    except Exception as e:
        logger.error(e)
        return 'Введите поисковый запрос...'