from django.conf import settings
from requests import get, exceptions
from datetime import datetime
from random import choice, randint
from json import loads
from .months import convert as month_convert
from .newsfilter import text_news_filter as filter_news
import logging


token = settings.NEWSAPI_TOKEN

def __main__() -> list:
    if randint(0, 100) > 70:
        error_http=False;error_json=False
        url = 'https://rapid-art.koval.workers.dev/'
        rand_token = choice(token)
        params = {'apiKey': rand_token}
        data_array = []
        try:
            http_response = get(url, params=params)
        except exceptions.RequestException:
            error_http = True
        if not error_http:
            json_response = loads(http_response.text)
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
                    ]
                    data_array.append(data_array_pre)
                logging.debug(f'Successfully loaded news. (Token: {rand_token})')
                logging.info('Successfully loaded news.')
                return data_array
        if error_http or error_json:
            logging.error(f'Error http: {error_http}; Error json: {error_json};')
    else:
        logging.debug('The news feed was not released because not enough was dropped.')
    return [['', '', '', '', '']]


def __test__():
    data = __main__()
    print(
        'Response data:', data,
        '\nLength:', len(data),
    )
