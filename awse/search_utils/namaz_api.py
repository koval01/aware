from json import loads
from datetime import datetime
import logging, requests_cache

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession(backend='memory', cache_name='namaz_get', expire_after=7200)

def get_result(city) -> dict:
    """
    Search by city name
    :param city: Search city name
    :return: Dictionary result
    """
    u = 'https://api.aladhan.com/v1/calendarByAddress'
    params = {
        'address': city,
    }
    for i in range(5):
        try:
            r = session.get(u, params=params)

            if r.status_code == 200:
                return loads(r.text)['data']

        except Exception as e:
            logger.error(e)


def unix_time_to_day(unix_time) -> int:
    """
    Convert unix time to day number
    :param unix_time: unix time integer
    :return: day number
    """
    return int(datetime.utcfromtimestamp(int(unix_time)).strftime('%d'))


def get_namaz_data(city) -> list:
    """
    Prepare and return data
    :param city: city name
    :return: dict
    """
    data = get_result(city)
    d = int(datetime.now().strftime("%d"))

    return [
        dict(
            timings=["%s: %s" % (key, value) for key, value in i['timings'].items() if key != 'Sunset'],
            time=i['date']['readable'],
            hijri_year=i['date']['hijri']['year'],
            hijri_month=i['date']['hijri']['month']['en'],
            hijri_day=i['date']['hijri']['day'],
            timezone=i['meta']['timezone'],
            update_time=datetime.today().replace(microsecond=0),
        ) for i in data if d == unix_time_to_day(i['date']['timestamp']) or
                       d+1 == unix_time_to_day(i['date']['timestamp'])
    ]