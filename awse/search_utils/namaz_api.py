import logging
import requests_cache
from datetime import datetime

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession(backend='memory', cache_name='namaz_get', expire_after=7200)


def get_result(city) -> dict:
    """
    Search by city name
    :param city: Search city name
    :return: Dictionary result
    """
    u = 'https://api.pray.zone/v2/times/this_week.json'
    params = {
        'city': city.capitalize(),
    }
    for i in range(5):
        try:
            r = session.get(u, params=params)

            if r.status_code == 200:
                return r.json()["results"]

        except Exception as e:
            logger.error(e)


def unix_time_to_day(unix_time) -> int:
    """
    Convert unix time to day number
    :param unix_time: unix time integer
    :return: day number
    """
    return int(datetime.utcfromtimestamp(int(unix_time)).strftime('%d'))


def get_namaz_data(city) -> list or None:
    """
    Prepare and return data
    :param city: city name
    :return: dict
    """
    try:
        data = get_result(city)["datetime"]
        d = int(datetime.now().strftime("%d"))

        rp = lambda x: x.replace("-", ".")
        return [
            dict(
                timings=[
                    "%s: %s" % (key, value) for key, value in i['times'].items() if key not in ['Imsak', 'Sunset']
                ],
                time=rp(i['date']['gregorian']),
                hijri=rp(i['date']['hijri']),
                timezone="UTC",
                update_time=datetime.today().replace(microsecond=0),
            ) for i in data if (d + 1) == unix_time_to_day(i['date']['timestamp']) or
                               (d + 2) == unix_time_to_day(i['date']['timestamp'])
        ]
    except Exception as e:
        logger.warning(e)
