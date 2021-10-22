from requests import get
import logging

logger = logging.getLogger(__name__)


def get_data(ipaddress) -> dict:
    try:
        return get("http://ip-api.com/json/%s" % ipaddress).json()["countryCode"].lower()
    except Exception as e:
        logger.error("User country code get error - %s" % e)
