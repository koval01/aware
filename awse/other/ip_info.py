from requests import get
from ..views import logger


def get_data(ipaddress) -> dict:
    try:
        return get("http://ip-api.com/json/%s" % ipaddress).json()["countryCode"].lower()
    except Exception as e:
        logger.error("User country code get error - %s" % e)
