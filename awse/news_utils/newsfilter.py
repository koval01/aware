from bs4 import BeautifulSoup


def text_news_filter(string):
    # Remove the protocol from the links
    string = str(string).replace('https://', '').replace('http://', '')
    # Remove the markup.
    string = BeautifulSoup(string, 'lxml').text
    string = string.replace('\n', '<br/>').replace('\'', '\\\'')
    if string == 'None':
        return 'The news has no description.'
    return string


def parse_text(string):
    if string:
        return BeautifulSoup(string, 'lxml').text.replace('\n', '%0A')
    else:
        return ""
