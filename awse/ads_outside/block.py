import logging
from random import randint
from time import time

from ..models import Info

logger = logging.getLogger(__name__)


def global_func(lang: str) -> dict or None:
    """
    Global feature for getting advertising
    :param lang: Language (language code)
    :return: Dictionary with data
    """
    valid_codes_lang = ['ua', 'ru', 'en']

    if not lang or lang not in valid_codes_lang: lang = "en"

    obj = Info.objects
    all_data = obj.all().filter(i_language=lang, i_active='yes')

    if all_data.count():
        logger.debug("%s: data count - %d" % (global_func.__name__, all_data.count()))

        max_retry = round(200 / (obj.count() / 4))
        if max_retry < 1: max_retry = 1

        for _ in range(max_retry):
            if obj.exists():
                for i in all_data:
                    if i.i_chance >= randint(1, 100) \
                            and randint(1, 6) > randint(1, 6) \
                            and round(time()) < round(i.i_time_active.timestamp()):
                        obj.filter(id=i.id).update(i_views=i.i_views + 1)  # Add one view

                        return i
