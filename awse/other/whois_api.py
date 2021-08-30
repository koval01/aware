import logging

import requests_cache

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession(backend='memory', cache_name='whois_api', expire_after=7200)


def get_info_domain(domain_name: str) -> str:
    """
    Get domain information
    :param domain_name: Domain name, example - telegram.org
    :return: Domain info into json
    """
    url = 'https://dns.google/resolve'

    try:
        data = session.get(url, params={
            "name": domain_name,
        }).json()
        return data
    except Exception as e:
        logger.error(e)
