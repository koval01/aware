from django.conf import settings
import logging, requests_cache

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession(backend='memory', cache_name='heroku_api', expire_after=7200)


def get_last_build_id() -> str:
    """
    Get latest build id from Heroku App
    :return: Latest build id
    """
    url = 'https://api.heroku.com/apps/%s/builds' % settings.HEROKU_APP_NAME

    headers = {
        'Accept': 'application/vnd.heroku+json; version=3',
        'Authorization': 'Bearer %s' % settings.HEROKU_API_KEY,
        'Range': 'created_at ..; order=desc',
    }

    try:
        data = session.get(url, headers=headers).json()

        if len(data) > 1 and not settings.DEBUG:
            return str(data[0]['id'])[0:8]

        else:
            return 'DEV_BUILD'

    except Exception as e:
        logger.error(e)
        return 'null'
