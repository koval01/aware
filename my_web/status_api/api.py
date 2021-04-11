from .config import USER_AGENT, API_URL, error_check_code
from json import loads
import logging, requests_cache

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession('status_get', expire_after=7200)


def __main__() -> dict:
    error_http=False;error_json=False
    headers = {"user-agent": USER_AGENT}
    try:
        http_response = session.get(API_URL, headers=headers)
    except Exception as e:
        logger.error(e)
        error_http = True
    if not error_http:
        json_response = loads(http_response.text)
        if json_response['status'] != 'ok': error_json = True
        if not error_json:
            m = json_response['monitor']
            data_array = dict(
                days7=m['7dRatio']['ratio'],
                days1=m['1dRatio']['ratio'],
                days30=m['30dRatio']['ratio'],
                days90=m['90dRatio']['ratio'],
                logs=m['logs'],
            )
            return data_array
    if error_http or error_json:
        logging.error(f'Error http: {error_http}; Error json: {error_json}; Code: %s;' % error_check_code)


def status_api() -> dict:
    """
    Функція для виклику Status API
    :return: Словник з даними
    """
    return __main__()