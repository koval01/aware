from django.conf import settings
import logging, requests_cache

logger = logging.getLogger(__name__)
USER_AGENT = settings.REQ_USER_AGENT
session = requests_cache.CachedSession(backend='memory', cache_name='search_complete_cache')


def get_result(question) -> str:
    """
    Get search data
    :param question: Search string
    :return: response dict
    """
    for i in range(3):
        try:
            headers = {
                "referer": "https://www.google.com/",
                "User-Agent": USER_AGENT,
            }

            params = {
                "q": question,
                "cp": len(question),
                "client": "gws-wiz",
                "xssi": "t",
                "gs_ri": "gws-wiz",
                "hl": "en-US",
            }

            r = session.get("https://www.google.com/complete/search", headers=headers, params=params)

            if r.status_code == 200:
                return r.text

        except Exception as e:
            logger.error(e)


def data_prepare(data) -> list:
    """
    Data preparation
    :param data: Incoming data
    :return: Output data
    """
    x = data.replace(")]}'", '')

    return eval(x)


def get_result_data(question) -> str:
    """
    Getting the final result
    :param question: Search bar
    :return: Result in time format
    """
    d = get_result(question)
    r = data_prepare(d)

    return ''.join(['<li class="search-el-a"><span class="ico_s_el" style="margin-right: 0.5em;"><i style="color: #9a9a9a;" class="fas fa-search"></i></span><span class="text_s_el">%s</span></li>' % i[0].replace('\\', '') for i in r[0]])