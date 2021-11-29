import logging
from random import randint
from time import time

from ..models import Banner

logger = logging.getLogger(__name__)


def global_func() -> dict or None:
    """
    Global function for getting banners
    :return: Dictionary with data
    """
    obj = Banner.objects
    all_data = obj.all().filter(active='yes')

    if all_data.count():
        logger.debug("%s: data count - %d" % (global_func.__name__, all_data.count()))

        max_retry = round(200 / (obj.count() / 4))
        if max_retry < 1: max_retry = 1

        for _ in range(max_retry):
            if obj.exists():
                for i in all_data:
                    if i.chance >= randint(1, 100) \
                            and randint(1, 6) > randint(1, 6) \
                            and round(time()) < round(i.time_active.timestamp()):
                        obj.filter(id=i.id).update(views=i.views + 1)
                        return i
