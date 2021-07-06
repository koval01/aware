from django.conf import settings
from datetime import datetime
from random import choice
from json import loads
from .newsfilter import text_news_filter as filter_news
import logging, requests_cache

token = settings.NEWSAPI_TOKEN
logger = logging.getLogger(__name__)
session = requests_cache.CachedSession('news_api_cache', expire_after=3600)


def __main__(news_append, get_one=False) -> list:
    if news_append:
        error_http = False
        error_json = False
        url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'country': 'us',
            'category': 'general',
            'apiKey': choice(token),
        }
        data_array = []
        try:
            http_response = session.get(url, params=params)
            # print(http_response.text, http_response.url, http_response.status_code)
        except Exception as e:
            logger.error(e)
            error_http = True
        if not error_http:
            try:
                json_response = loads(http_response.text)
            except Exception as e:
                logger.error(e)
                error_json = True
            if not error_json:
                status_field = json_response['status']
                if str(status_field) != 'ok': error_json = True
                if not error_json:
                    for el in json_response['articles']:
                        time_field = datetime.fromisoformat(str(el['publishedAt'])[:-1])
                        time_field = time_field.strftime("%d %B %Y at %H:%M")
                        description = filter_news(el['description'])
                        if description == 'None' or not description:
                            description = 'The news does not contain a description'
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
                    if get_one:
                        return choice(data_array)

                    return data_array

        if error_http or error_json:
            logger.error(f'Error http: {error_http}; Error json: {error_json};')
    return [['' for x in range(6)] for y in range(100)]


def __test__():
    data = __main__()
    print(
        'Response data:', data,
        '\nLength:', len(data),
    )


def news_search(string) -> bool:
    """
    We offer AWARE news
    :param string: Search query
    :return: bulent result
    """
    words = [
        'новость', 'новости', 'новостей', 'новостью', 'новостям', 'новостями', 'новостях',
        'новина', 'новини', 'новин', 'новиною', 'новинам', 'новинами', 'новинах', 'news',
    ]
    for i in words:
        if i in string.lower():
            return True
