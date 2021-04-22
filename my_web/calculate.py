from math import *
import regex as re
import logging

logger = logging.getLogger(__name__)


def calculator(string) -> str:
    try:
        s = re.sub(r'[^-+*/:\()0-9.,\p{Latin}]+', '', string)
        s = s.replace(':', '/').replace('\\', '/')
        s = s.replace('import', '').replace('for', '').replace('while', '')
        return eval(s), s
    except Exception as e:
        logger.error(e)
        return '', ''
