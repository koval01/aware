import logging


# Month converter

def convert(string):
    en_mon = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']
    ru_mon = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
              'октября', 'ноября', 'декабря']
    for i in en_mon:
        string = string.replace(i, ru_mon[en_mon.index(i)])
        logging.debug(f'Converting "{i}" to "{ru_mon[en_mon.index(i)]}"')
    return string