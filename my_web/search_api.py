from json import loads
from .covid.config import USER_AGENT
from urllib.parse import urlparse, parse_qs
from django.conf import settings
from random import shuffle
from bs4 import BeautifulSoup
from string import punctuation
from .models import BlackWord
from .common_functions import similarity
import logging, requests_cache, \
    re, traceback

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession('search_api_cache', expire_after=259200)
null_search_dict = [['' for _ in range(6)] for y in range(100)]


def get_result(question, index=1) -> dict:
    """
    Get search data
    :param question: Search string
    :param index: search index element
    :return: response dict
    """
    u = settings.SEARCH_API_HOST
    keys = settings.SEARCH_API_KEYS.split()
    cx = settings.SEARCH_CX
    shuffle(keys)
    for i, e in enumerate(keys):
        try:
            headers = {
                "User-Agent": USER_AGENT,
            }
            params = {
                "key": keys[i],
                "cx": cx,
                "q": question,
                "queries": 10,
                "safe": 'active',
                "start": index,
            }
            r = session.get(u, headers=headers, params=params)
            if r.status_code != 200:
                logger.error("%s (LEN:%s) %s %s" % (keys[i], len(keys), r.status_code, loads(r.text)['error']['message']))
            else:
                return loads(r.text)
        except Exception as e:
            logger.error(e)


def search_youtube(link) -> dict:
    """
    Перевірка чи веде посилання на YouTube
    :return: ID відео або None, якщо не веде на YouTube
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
    Пошук слів у результатах із запиту користувача
    :param search_text: Текст пошукового запиту
    :param result_text: Текст результату пошуку
    :return: Відредагований текст для результату
    """
    tag_template = '<b style="color: #808080;text-decoration: underline;">%s</b>'

    symbols = punctuation.replace('', ' ').split()

    for i in symbols:
        search_text = search_text.replace(i, ' ')

    only_letters_search = ''.join(w for w in search_text if w.isalpha() or w == ' ')
    result = result_text

    for i in only_letters_search.split():
        if len(i) >= 3:
            x = re.findall(i, result, flags=re.I)
            for w in x:
                result = result.replace(w, tag_template % w)

    return result.replace('> <', '>&nbsp;<')


def data_prepare(data, search_text) -> dict:
    """
    Обробка і підготовка даних
    :param data: Масив з даними
    :param search_text: Пошуковий запит
    :return: Сформований масив даних
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
                    snippet = BeautifulSoup(
                        i['snippet'], 'lxml'
                    ).text
                except Exception as e:
                    snippet = '...'
                    logger.warning(e)

                try:
                    thumb = i['pagemap']['cse_thumbnail'][0]['src']
                except Exception as e:
                    thumb = None
                    logger.warning(e)

                split_snippet = str(snippet).split()
                array_done = []

                for x in split_snippet:
                    if len(x) > 27:
                        x = x[:27]+"..."
                    array_done.append(x)
                snippet = " ".join(array_done)

                snippet = search_words_in_result(search_text, snippet)
                yt = search_youtube(i['link'])

                array.append(dict(
                    title=i['title'],
                    link=i['link'],
                    displayLink=i['displayLink'],
                    snippet=snippet,
                    thumb=thumb,
                    youtube=yt['link'],
                    youtube_id=yt['id'],
                ))
    except Exception as e:
        logger.error(traceback.print_tb(e.__traceback__))

    return dict(s_info=s_info, array=array)


def check_words_in_search_string(search_string) -> bool:
    """
    Функція яка перевіряє пошукову стрічку на наявність заборонених слів
    :param search_string: Пошукова строка
    :return: Результат перевірки (bool)
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
    Функція пошуку
    :param string: Пошуковий запит
    :return: Список результатів
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
    Функція пошуку
    :param string: Пошуковий запит
    :param index: Пошуковий індекс
    :return: Список результатів
    """
    x = get_result(string, index)
    d = data_prepare(x, string)
    return dict(data=d['s_info'], array=d['array'])


def select_type(string, index) -> dict:
    """
    Функція для зручного вибору режиму
    :param string: Пошукова строка
    :param index: Індекс
    :return: результат пошуку
    """
    x = check_words_in_search_string(string)

    if x and not index:
        return dict(data=[], array=null_search_dict, error=True)
    elif x and index:
        return dict(data=[], array=null_search_dict, error=True)

    if index:
        return search_custom_index(string, index)
    return search(string)