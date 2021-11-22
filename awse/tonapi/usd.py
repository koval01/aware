from requests import get
from json import loads

from config import USD_SOURCE_URL
import re
import logging


class UsdPriceTon:
    def __init__(self) -> None:
        self.url = USD_SOURCE_URL
        self.pattern = '<script type="application/ld\+json">.*?</script>'
        self.tag_pattern = '<.*?>'

    def get_page(self) -> str:
        response = get(self.url)
        if response.status_code >= 200 < 400 \
                and len(response.text) > 1000:
            return response.text

    def check_data(self, page) -> dict:
        try:
            founded_array = re.findall(self.pattern, page)
            if founded_array:
                vars = loads(re.sub(r"<.*?>", "", founded_array[0]))
                if vars["currency"] == "TONCOIN" \
                        and vars["currentExchangeRate"]["priceCurrency"] == "USD":
                    return vars
        except Exception as e:
            logging.warning(e)

    def price(self, page) -> float:
        validator = self.check_data(page)
        return validator["currentExchangeRate"]["price"]

