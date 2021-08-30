import logging
import requests_cache
from datetime import datetime
from random import choice

from django.conf import settings

from ..news_utils.newsfilter import parse_text
from ..news_utils.newsfilter import text_news_filter as filter_news

token = settings.NEWSAPI_TOKEN
logger = logging.getLogger(__name__)
session = requests_cache.CachedSession(backend="memory", namespace='news_api_cache', expire_after=3600)
available_country = settings.AVAILABLE_COUNTRY


def __main__(country_code: str) -> list:
    """
    Function for get news list by country user
    :param country_code: Country code for search news
    :return list: news list
    """
    if country_code in available_country:
        error_http = False
        error_json = False

        url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'apiKey': choice(token),
            'country': country_code,
            'category': 'general',
        }
        data_array = []

        try:
            http_response = session.get(url, params=params)
        except Exception as e:
            logger.error(e)
            error_http = True

        if not error_http:
            try:
                json_response = http_response.json()
            except Exception as e:
                logger.error(e)
                error_json = True

            if not error_json:
                status_field = json_response['status']

                if str(status_field) != 'ok':
                    error_json = True

                if not error_json:
                    for el in json_response['articles']:
                        desc_org = parse_text(el['description']).replace('\'', '\\\'')

                        time_field = datetime.fromisoformat(el['publishedAt'][:-1])
                        el['publishedAt'] = round(time_field.timestamp()) * 1000

                        el['description'] = filter_news(el['description'])
                        el['title'] = filter_news(el['title'])
                        el['source']['name'] = el['source']['name'].replace('\'', '\\\'')

                        if len(el['source']['name']) > 20:
                            el['source']['name'] = (el['source']['name'])[:17] + "..."

                        if not el['description']:
                            el['description'] = el['title']

                        data_array_pre = dict(
                            title=el['title'],
                            description=el['description'],
                            name=el['source']['name'],
                            time=el['publishedAt'],
                            url=el['url'],
                            image=el['urlToImage'],
                            source_mark=el['source']['name'],
                            desc_org=desc_org,
                        )
                        data_array.append(data_array_pre)

                    return data_array

            if error_http or error_json:
                logger.error(f'Error http: {error_http}; Error json: {error_json};')

    return []
