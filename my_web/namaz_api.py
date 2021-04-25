from requests import get
from json import loads
from .months import convert_short
import logging

logger = logging.getLogger(__name__)


def get_result(city) -> dict:
    """
    Search by city name
    :param city: Search city name
    :return: Dictionary result
    """
    u = 'http://api.aladhan.com/v1/calendarByAddress'
    params = {
        'address': city,
    }
    try:
        r = get(u, params=params)
        if r.status_code == 200:
            return loads(r.text)['data']
    except Exception as e:
        logger.error(e)


def get_namaz_data(city) -> list:
    """
    Prepare and return data
    :param city: city name
    :return: dict
    """
    data = get_result(city)
    return [dict(
        timings=["%s: %s" % (key, value) for key, value in data['timings'].items()],
        time=convert_short(data['date']['readable']),
    ) for _ in data]