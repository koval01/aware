import logging


# Module for filtering the context of the news feed

def text_news_filter(string):
    # Remove the protocol from the links
    string = str(string).replace('https://', '').replace('http://', '')
    # Remove the markup.
    string = string.replace('&raquo;', '').replace('&laquo;', '').replace('&nbsp;', '')
    string = string.replace('\n', '').replace('\r', '').replace('\t', '')
    logging.debug('News feed successfully filtered.')
    return string