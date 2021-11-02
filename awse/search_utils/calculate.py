import logging

import regex as re

logger = logging.getLogger(__name__)


def calculator(string: str) -> tuple:
    bad_list = ['import', 'for', 'while', 'exit', 'from', 'lambda', 'os', '_']
    try:
        s = string.lower().replace('×', '*').replace(',', '.')
        for e in ['π', 'п']: s = s.replace(e, 'pi')
        for e in [':', '\\']: s.replace(e, '/')
        for e in bad_list: s.replace(e, '')
        s = re.sub(r"random(.*?)", "random()", s)
        s = re.sub(r'[^-+*/:\()0-9.,\s\p{Latin}]+', '', s)

        if any(word in s for word in ['+', '-', '*', '/']):
            return eval(s), s
        else: return '', ''

    except Exception as e:
        logger.error(e)
        return '', ''
