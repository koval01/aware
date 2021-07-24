import logging
import re
import requests_cache
import traceback
from json import loads
from random import shuffle
from string import punctuation
from urllib.parse import urlparse, parse_qs

from django.conf import settings

from awse.common_functions import similarity
from django.conf import settings
from awse.models import BlackWord

logger = logging.getLogger(__name__)
USER_AGENT = settings.REQ_USER_AGENT
session = requests_cache.CachedSession(backend='memory', cache_name='search_api_cache', expire_after=259200)
null_search_dict = [['' for _ in range(6)] for y in range(100)]


def get_result(question, index=1, search_type='searchTypeUndefined') -> dict:
    """
    Get search data
    :param question: Search string
    :param index: search index element
    :param search_type: search type
    :return: response dict
    """
    u = settings.SEARCH_API_HOST
    keys = settings.SEARCH_API_KEYS.split()
    cx = settings.SEARCH_CX
    shuffle(keys)
    for i, e in enumerate(keys):
        queries = 10
        if search_type == 'image':
            queries = queries * 2
        try:
            headers = {
                "User-Agent": USER_AGENT,
            }
            params = {
                "key": keys[i],
                "cx": cx,
                "hl": "en",
                "q": question,
                "queries": queries,
                "safe": 'active',
                "start": index,
                "searchType": search_type,
            }
            r = session.get(u, headers=headers, params=params)
            if r.status_code != 200:
                logger.error(
                    "%s (LEN:%s) %s %s" % (keys[i], len(keys), r.status_code, loads(r.text)['error']['message']))
            else:
                logger.warning("%s..." % (r.text[:256]))

                return loads(r.text)

        except Exception as e:
            logger.error(e)


def search_youtube(link) -> dict:
    """
    Check whether the link is on YouTube
    :return: Video ID or None if not hosted on YouTube
    """
    domains = [
        'youtube.com', 'youtu.be',
    ]
    url = urlparse(link)

    try:
        if re.search(domains[0], link):
            video_id = parse_qs(url.query)['v'][0]

        elif re.search(domains[1], link):
            video_id = url.path.replace('/', '')

        else:
            return dict(link=None, id=None)

        # v = pafy.new(video_id)
        # id_ = v.streams[0].url_https

        return dict(link=None, id=video_id)

    except Exception as e:
        logger.warning(e)

    return dict(link=None, id=None)


def search_words_in_result(search_text, result_text) -> str:
    """
    Search for words in the results of a user query
    :param search_text: Search query text
    :param result_text: Search result text
    :return: Edited text for the result
    """
    tag_template = '<b class="text_select_in_results">%s</b>'

    symbols = punctuation.replace('', ' ').split()
    # get punctuation symbols

    for i in symbols:
        search_text = search_text.replace(i, ' ')

    only_letters_search = ''.join(w for w in search_text if w.isalpha() or w == ' ')
    result = result_text
    used = []

    for i in only_letters_search.split():
        if len(i) >= 3:
            x = re.findall(i, result, flags=re.I)
            for w in x:
                if w not in used:
                    used.append(w)
                    result = result.replace(w, tag_template % w)

    return result


def data_prepare(data, search_text) -> dict:
    """
    Data processing and preparation
    :param data: Data array
    :param search_text: Search query
    :return: An array of data is formed
    """
    try:
        if data['searchInformation']['totalResults']:
            array = []
            s = data['searchInformation']
            s_info = dict(
                formattedSearchTime=s['formattedSearchTime'],
                formattedTotalResults=s['formattedTotalResults'],
            )
            for i in data['items']:
                try:
                    thumb = i['pagemap']['cse_thumbnail'][0]['src']
                except Exception as e:
                    thumb = None
                    logger.warning(e)

                yt = search_youtube(i['link'])

                array.append(dict(
                    title=i['title'],
                    link=i['link'],
                    displayLink=i['displayLink'],
                    snippet=i['htmlSnippet'].replace('<br>', '').replace(
                        '<b>', '<b class="text_select_in_results">'),
                    thumb=thumb,
                    youtube=yt['link'],
                    youtube_id=yt['id'],
                ))
    except Exception as e:
        logger.error(traceback.print_tb(e.__traceback__))

    return dict(s_info=s_info, array=array)


def check_words_in_search_string(search_string) -> bool:
    """
    A function that checks the search bar for banned words
    :param search_string: Search term
    :return: Bool result
    """
    for i in search_string.split():
        alpha = ''.join(filter(str.isalpha, i)).capitalize()

        for word in BlackWord.objects.values('word'):
            word = word['word']

            if alpha.lower() == word.lower():
                return True

            if similarity(alpha, word) >= 0.85:
                if BlackWord.objects.filter(word=word.capitalize()).values('ano_mode')[0]['ano_mode'] == 'yes':
                    return True


def search(string) -> dict:
    """
    Search function
    :param string: Search query
    :return: List of results
    """

    def search_error():
        return dict(data='', array=null_search_dict, error=True)

    try:
        if not string:
            return search_error()

        array = []
        for i in range(2):
            if i == 0:
                s = 1
            else:
                s = i * 10 + 1
            x = get_result(string, s)
            d = data_prepare(x, string)
            if i == 1:
                data = d['s_info']
            array = array + d['array']
        return dict(data=data, array=array, error=False)
    except Exception as e:
        logger.warning(e)
        return search_error()


def search_custom_index(string, index) -> dict:
    """
    Search function
    :param string: Search query
    :param index: Search index
    :return: List of results
    """
    x = get_result(string, index)
    d = data_prepare(x, string)
    return dict(data=d['s_info'], array=d['array'])


def select_type(string, index, search_type='searchTypeUndefined') -> dict:
    """
    Function for easy mode selection
    :param string: Search term
    :param index: Index
    :param search_type: search type
    :return: search result
    """
    x = check_words_in_search_string(string)

    if search_type == 'searchTypeUndefined':
        if x and not index:
            return dict(data=[], array=null_search_dict, error=True)
        elif x and index:
            return dict(data=[], array=null_search_dict, error=True)

        if index:
            return search_custom_index(string, index)

        return search(string)

    else:
        return get_result(string, 0, search_type)
