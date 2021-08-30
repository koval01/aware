import logging
import requests_cache
from datetime import datetime
from json import loads
from random import shuffle

from django.conf import settings

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession(backend='memory', cache_name='search_api_cache', expire_after=600)
api_keys = str(settings.WEATHER_API_KEYS).split()
shuffle(api_keys)


def weather_get(string) -> dict:
    """
    Отримання даних про погоду
    :param string: Строка в якій потрібно знайти назву міста
    :return: Array result
    """
    if string:
        for key in api_keys:
            u = 'https://api.openweathermap.org/data/2.5/weather'
            a_string = string.split()
            for city in a_string:
                for i in range(5):
                    city_local = city

                    if i:
                        city_local = city[:-1]

                    if i > 1:
                        city_local = city[:-1] + 'а'

                    if i > 2:
                        city_local = city[:-2] + 'ы'

                    if i > 3:
                        city_local = city + 'е'

                    def check_word(city_in_func) -> bool:
                        """
                        Внутрішня функція для перевірки неправильних назв
                        :param city_in_func: Отримана назва міста
                        :return: Булентний результат
                        """
                        city_in_func = city_in_func.lower()
                        words = {
                            'кака', 'по', 'город',
                        }

                        return set(city_in_func.split()) & words

                    if not check_word(city_local):

                        params = {
                            'q': city_local,
                            'appid': key,
                            'lang': 'en',
                            'units': 'metric',
                        }

                        if weather_words(string):
                            try:
                                r = session.get(u, params=params).text
                                result = loads(r)
                                if result['cod'] == 200:
                                    return dict(
                                        now_weather=result,
                                        future_weather=weather_by_days_get(city_local),
                                    )

                            except Exception as e:
                                logger.error(e)


def weather_by_days_get(city) -> list:
    """
    Отримання даних про погоду по днях (12:00)
    :param city: Строка в якій потрібно знайти назву міста
    :return: Array result
    """
    if city:
        for key in api_keys:
            u = 'https://api.openweathermap.org/data/2.5/forecast'
            params = {
                'q': city,
                'appid': key,
                'lang': 'ru',
                'units': 'metric',
            }

            try:
                r = session.get(u, params=params).text
                result = loads(r)
                if result['cod'] == "200":
                    return [b for b in result['list'] if '09:00:00' in b['dt_txt'] and
                            datetime.fromtimestamp(b['dt']).day != datetime.now().day
                            ]

            except Exception as e:
                logger.error(e)


def get_weather_icon(code) -> str:
    """
    Визначення піктограми
    :param code: код погоди
    :return: HTML код
    """
    if code == '01d' or code == '01n':
        return '<i class="fas fa-sun"></i>'

    elif code == '02d' or code == '02n':
        return '<i class="fas fa-cloud-sun"></i>'

    elif code == '03d' or code == '03n':
        return '<i class="fas fa-cloud"></i>'

    elif code == '04d' or code == '04n':
        return '<i class="fas fa-cloud"></i>'

    elif code == '09d' or code == '09n':
        return '<i class="fas fa-cloud-showers-heavy"></i>'

    elif code == '10d' or code == '10n':
        return '<i class="fas fa-cloud-sun-rain"></i>'

    elif code == '11d' or code == '11n':
        return '<i class="fas fa-poo-storm"></i>'

    elif code == '13d' or code == '13n':
        return '<i class="far fa-snowflake"></i>'

    elif code == '50d' or code == '50n':
        return '<i class="fas fa-smog"></i>'


def weather_words(string) -> list:
    """
    Перевірка строки, чи пов'язана вона з погодою
    :param string: Стока яку потрібно перевірити
    :return: Результат перевірки
    """
    words = {
        'погода', 'погоды', 'погоде', 'погоду', 'погодой', 'погодою', 'погодах', 'погодами', 'погодам',
        'weather',
    }

    string = string.lower()
    in_data = set(string.split()) & words

    return [True for i in words if in_data]
