from django.conf import settings
from requests import get, exceptions
from datetime import datetime
from random import choice
from json import loads
from .months import convert as month_convert
from .newsfilter import text_news_filter as filter_news
import logging


token = settings.NEWSAPI_TOKEN

def __main__(news_append) -> list:
    if news_append:
        error_http=False;error_json=False
        url = 'https://rapid-art.koval.workers.dev/'
        params = {'apiKey': choice(token)}
        data_array = []
        try:
            http_response = get(url, params=params)
        except exceptions.RequestException:
            error_http = True
        if not error_http:
            try:
                json_response = loads(http_response.text)
            except Exception as e:
                logging.error(e)
                error_json = True
            if not error_json:
                status_field = json_response['status']
                if str(status_field) != 'ok': error_json = True
                if not error_json:
                    for el in json_response['articles']:
                        time_field = datetime.fromisoformat(str(el['publishedAt'])[:-1])
                        d_ = time_field.strftime("%d %B %Y г. %H:%M")
                        time_field = month_convert(d_)
                        description = filter_news(el['description'])
                        title = filter_news(el['title'])
                        data_array_pre = [
                            title,
                            description,
                            el['source']['name'],
                            time_field,
                            el['url'],
                            el['urlToImage'],
                        ]
                        data_array.append(data_array_pre)
                    logging.info('Successfully loaded news.')
                    return data_array
        if error_http or error_json:
            logging.error(f'Error http: {error_http}; Error json: {error_json};')
    return [['' for x in range(6)] for y in range(20)]


def __test__():
    data = __main__()
    print(
        'Response data:', data,
        '\nLength:', len(data),
    )
