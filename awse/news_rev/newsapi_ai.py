import logging
import requests_cache
from datetime import datetime
from random import choice

from django.conf import settings

token = settings.NEWSAPI_TOKEN
logger = logging.getLogger(__name__)
session = requests_cache.CachedSession(backend="memory", namespace='news_api_ai_cache', expire_after=300)
available_country = settings.AVAILABLE_COUNTRY


def __main__(country_code: str, max_pages: int) -> list:
    """
    Function for get news list by country user
    :param country_code: Country code for search news
    :return list: news list
    """
    if country_code in available_country:
        error_http = False
        error_json = False

        query = [
            'Зеленський', 'Суддя', 'Слідчий', 'Прокурор', 'Позив', 'Рішення',
        ]

        url = 'https://eventregistry.org/api/v1/article/getArticles'
        params = {
            "apiKey": settings.NEWSAPI_AI,
            "action": "getArticles",
            "keyword": choice(query),
            "articlesPage": 1,
            "articlesCount": max_pages,
            "articlesSortBy": "date",
            "articlesSortByAsc": False,
            "articlesArticleBodyLen": -1,
            "resultType": "articles",
        }
        data_array = []

        try:
            http_response = session.get(url, params=params)
            logger.info("Status response NEWS API AI: %s" % http_response.status_code)
        except Exception as e:
            logger.error(e)
            error_http = True

        try:
            if not error_http:
                try:
                    json_response = http_response.json()
                except Exception as e:
                    logger.error(e)
                    error_json = True

                if not error_json:
                    for el in json_response['articles']['results']:
                        el['dateTime'] = round(datetime.strptime(el['dateTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
                            tzinfo=None).timestamp()) * 1000

                        if len(el['source']['title']) > 20:
                            el['source']['title'] = (el['source']['title'])[:17] + "..."

                        if el['lang'] == 'ukr' and len(el['body']) > 32:
                            data_array_pre = dict(
                                title=el['title'],
                                description=el['body'],
                                name=el['source']['title'],
                                time=el['dateTime'],
                                url=el['url'],
                                image=el['image'],
                                source_mark=el['source']['title'],
                                # desc_org=desc_org,
                            )
                            data_array.append(data_array_pre)

                    return data_array

                if error_http or error_json:
                    logger.error(f'(NewsApi_AI) Error http: {error_http}; Error json: {error_json};')

        except Exception as e:
            logger.warning(e)

    return []
