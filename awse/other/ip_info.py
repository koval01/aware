from requests import get


def get_data(ipaddress) -> dict:
    return get("http://ip-api.com/json/%s" % ipaddress).json()
