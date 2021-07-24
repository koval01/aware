from math import *
import regex as re
import logging

logger = logging.getLogger(__name__)


def calculator(string) -> str:
    try:
        s = string.lower().replace('×', '*').replace('π', 'pi').replace('п', 'pi')
        s = re.sub(r'[^-+*/:\()0-9.,\s\p{Latin}]+', '', s)
        s = s.replace(':', '/').replace('\\', '/')
        s = s.replace('import', '').replace('for', '').replace('while', '')
        if any(word in s for word in ['+', '-', '*', '/']):
            return eval(s), s
        else:
            return '', ''
    except Exception as e:
        logger.error(e)
        return '', ''