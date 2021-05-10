from bs4 import BeautifulSoup
import logging


def text_news_filter(string):
    """
    Remove other elements from text
    :param string: string
    :return: edited string
    """
    string = str(string).replace('https://', '').replace('http://', '')
    # Remove the markup.
    # string = string.replace('&raquo;', '').replace('&laquo;', '').replace('&nbsp;', '').replace(
    #         '&mdash;', '')
    # string = string.replace('\n', '').replace('\r', '').replace('\t', '')

    logging.debug('News feed successfully filtered.')

    return BeautifulSoup(string, 'lxml').text