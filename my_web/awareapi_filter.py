from urllib.parse import urlunsplit
from bs4 import BeautifulSoup
from requests import get
import logging, urllib, re

logger = logging.getLogger(__name__)
user_agent_static = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4469.3 Safari/537.36'


def get_html_code_page(link) -> str:
    """
    Getting html code website
    :param link: Link to page
    :return: html code page
    """
    try:
        r = get(link, headers={
            "User-Agent": user_agent_static
        }).text
    except Exception as e:
        logger.error(e)
        r = None
    return r


def get_body_el_page(page_html) -> dict:
    """
    Отримуємо тіло сторінки, знаходимо текстові теги і повертаємо це в строці, також ця функція передаю заголовок
    :param page_html: HTML код сторінки яку потрібно проаналізувати
    :return: Всі потрібні теги в строці
    """
    soup = BeautifulSoup(page_html, 'html.parser')
    try:
        title_page = soup.title.string
    except Exception as e:
        logger.error(e)
        title_page = 'Не удалось получить заголовок страницы'

    text_tags = [
        'p', 'i', 'b', 'code', 'em', 'strong',
        'mark', 'small', 'sub', 'sup', 'ins', 'del',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img',
    ]
    tags_list = soup.find_all(text_tags)
    html = []
    for i in tags_list:
        x = str(i).replace('h1', 'h4').replace('h2', 'h5').replace('h3', 'h6')
        soup = BeautifulSoup(x, 'html.parser')
        for s in soup.select('script'):
            s.extract()
        html.append(str(soup))
    html = ''.join(html)
    return dict(title=title_page, html=html)


def get_youtube_link(link) -> str:
    """
    Якщо посилання на ютуб, то обробляємо його, якщо ні, то повертаємо None
    :param link: Посилання на сайт
    :return: Результат у форматі строки
    """
    yt = False
    if 'youtube.com/watch?v=' in link:
        url = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(link).query))
        link_video = url['v'];
        yt = True
    elif 'youtu.be/' in link:
        url = urllib.parse.urlsplit(link).path
        link_video = url;
        yt = True
    if yt:
        r = f'<iframe width="auto" height="auto" style="width:100%;" src="https://www.youtube.com/embed/{link_video}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        return r


def get_instant_page(link) -> dict:
    """
    Функція для зручного отримання посилання на Instant View сторінку
    :param link: Посилання яке потрібно обробити
    :return: Title, html code, template id
    """
    page = get_html_code_page(link)
    data = get_body_el_page(page)
    try:
        yt = get_youtube_link(link)
    except Exception as e:
        logger.error(e)
        yt = None
    if yt:
        html = yt
    else:
        html = data['html']
    if bool(BeautifulSoup(html, "html.parser").find()):
        html = html
    else:
        html = '<p>Не удалось проанализировать эту страницу ... Простите.</p>'
    title = data['title']
    template = 'dd7f8f14ecc26f'  # Telegram Instant View template hash
    return dict(
        title=title, html=html, template=template,
    )
