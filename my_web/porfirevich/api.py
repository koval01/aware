from requests import get, exceptions
from datetime import datetime
from .config import USER_AGENT, API_URL, error_check_code
from json import loads
from ..months import convert as month_convert
import logging, re, string, random


def __main__() -> list:
    error_http=False;error_json=False
    headers = {"user-agent": USER_AGENT}
    data_array = []
    try:
        http_response = get(API_URL, headers=headers)
    except exceptions.RequestException:
        error_http = True
    if not error_http:
        json_response = loads(http_response.text)
        if not len(json_response['data']): error_json = True
        if not error_json:
            for el in json_response['data']:
                text = decode_story_string(el['content'])
                if error_check_code not in text and len(text) < 20000:
                    time_field = datetime.fromisoformat(str(el['createdAt'])[:-5])
                    d_ = time_field.strftime("%d %B %Y г. %H:%M")
                    time_field = month_convert(d_)
                    likes = el['likesCount']
                    data_array_pre = [
                        text,
                        time_field,
                        likes,
                        el['id'],
                    ]
                    data_array.append(data_array_pre)
            logging.info('Successfully loaded profirevich stories.')
            return data_array
    if error_http or error_json:
        logging.error(f'Error http: {error_http}; Error json: {error_json};')


def get_story(story_id) -> str:
    error_http=False;error_json=False
    headers = {"user-agent": USER_AGENT}
    url = 'https://porfirevich.ru/api/story/'+story_id
    try:
        http_response = get(url, headers=headers)
    except exceptions.RequestException:
        error_http = True
    if not error_http:
        json_response = loads(http_response.text)
        if not len(json_response['id']): error_json = True
        if not error_json:
            text = decode_story_string(json_response['content'])
            time_field = datetime.fromisoformat(str(json_response['createdAt'])[:-5])
            d_ = time_field.strftime("%d %B %Y г. %H:%M")
            time_field = month_convert(d_)
            likes = json_response['likesCount']
            id = json_response['id']
            if error_check_code in text:
                text = 'Эта запись не смогла пройти фильтрацию, поэтому её нельзя посмотреть.'
            else:
                logging.info('Successfully loaded profirevich story.')
            return text, time_field, likes, id
    if error_http or error_json:
        logging.error(f'Error http: {error_http}; Error json: {error_json};')


def prepare_data(data) -> list:
    """
    Data preparation
    """
    for i in data['data']:
        return i


def cleanhtml(raw_html) -> str:
    """
    Clearing the string from HTML tags
    :param raw_html: Input string
    :return: Filtered string
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def fix_string(string) -> str:
    """
    Removing extra spaces in text
    :param string: Input term
    :return: Filtered string
    """
    in_word = string
    in_between_words = ['-', '–']
    in_sentences = ['«', '(', '[', '{', '"', '„', '\'']
    for item in in_between_words:
        regex = r'\w[%s]\s\w' % item
        in_word = re.findall(regex, string)

        for x in in_word:
            a = x[:1]; b = x[3:4]
            string = string.replace(x, a + '-' + b)

    for item in in_sentences:
        string = string.replace(f' {item} ', f' {item}')
    return string


def check_long_words_in_string(string) -> bool:
    """
    Проверка наличия слишком довгих слов/елементов в строке
    """
    status = True
    s = string.split()
    for i in s:
        if len(i) > 29:
            status = False

    return status


def decode_story_string(array) -> str:
    """
    Декодер текста записи
    """
    struct_array = []
    array = loads(array)
    for i in array:
        text = cleanhtml(i[0])
        text = fix_string(text)
        if check_long_words_in_string(text):
            text = text.replace('\n', '</br>')
            if i[1]:
                struct_array.append(f'<b id="{get_random_string()}">{text}</b>')
            else:
                struct_array.append(f'<i id="{get_random_string()}">{text}</i>')
        else:
            struct_array.append(f'<b id="{get_random_string()}">{error_check_code}</b>')
    return ''.join(struct_array)


def get_random_string(length = 0) -> str:
    """
    Генерация рандомной строки из цифр и букв
    """
    if length == 0: length = random.randint(8, 32)
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# def gen_link_porfirevich(post_id) -> str:
#     """
#     Простая генерация ссылки на запись
#     """
#     link = '<a id="%s" href="https://www.q-writer.com/story/%s">История Порфирьевича</a>' % (get_random_string(), post_id)
#     return link