import logging

ua_month = ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня',
            'вересня', 'жовтня', 'листопада', 'грудня']
ru_month = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
            'октября', 'ноября', 'декабря']
en_month = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december']


def convert(string) -> str:
    """
    Full mont name converter
    :param string: string date
    :return: formatted string
    """
    en_mon = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']
    ru_mon = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
              'октября', 'ноября', 'декабря']
    for i in en_mon:
        string = string.replace(i, ru_mon[en_mon.index(i)])
        logging.debug(f'Converting "{i}" to "{ru_mon[en_mon.index(i)]}"')
    return string


def convert_short(string) -> str:
    """
    short month name converter
    :param string: string date
    :return: formatter string
    """
    en_mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ru_mon = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
              'октября', 'ноября', 'декабря']
    for i in en_mon:
        string = string.replace(i, ru_mon[en_mon.index(i)])
        logging.debug(f'Converting "{i}" to "{ru_mon[en_mon.index(i)]}"')
    return string
