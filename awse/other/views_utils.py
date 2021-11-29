import logging

from cryptography.fernet import Fernet
from django.conf import settings

logger = logging.getLogger(__name__)

img_link_proxy_key = settings.IMAGE_PROXY_LINK_KEY
sign_key = settings.SIGN_ENCRYPT_KEY


def link_enc_img(link) -> str:
    try:
        salt_link = Fernet(img_link_proxy_key)
        data_link = str.encode(str(link))
        result = salt_link.encrypt(data_link).decode("utf-8")

        return result

    except Exception as e:
        logger.error("%s: %s" % (link_enc_img.__name__, e))


def sign_adr_enc(address) -> str:
    try:
        salt_sign = Fernet(sign_key)
        data_sign = str.encode(str(address))
        result = salt_sign.encrypt(data_sign).decode("utf-8")
        return result

    except Exception as e:
        logger.error("%s: %s" % (sign_adr_enc.__name__, e))
