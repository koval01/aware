from requests import get
from json.decoder import JSONDecodeError
import logging

from bs4 import BeautifulSoup


class WikipediaSearchModule:
    def __init__(self, search_text) -> None:
        """
        Initialize Wikipedia search module
        :param search_text: Searching text
        :return: Init
        """
        self.params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "utf8": 1,
        }
        self.search_text = search_text

    def request(self, search_text) -> dict:
        """
        Make request to Wikipedia API
        :param search_text: Searching text
        :return: JSON data in python dictionary
        """
        try:
            self.params["srsearch"] = search_text
            return get(
                "https://en.wikipedia.org/w/api.php",
                params=self.params
            ).json()
        except JSONDecodeError as e:
            logging.error("Wikipedia search API error parse json response, details: %s" % e)
        except Exception as e:
            logging.error("Wikipedia search API error make request, details: %s" % e)

    def beautiful_soup_filter(self, text) -> str:
        return BeautifulSoup(text, 'lxml').text

    def parser(self, data) -> dict:
        """
        Parse ordered items
        :param data: JSON data converted to dictionary
        :return: Items in dictionary
        """
        try:
            data = data["query"]["search"][0]
            data["snippet"] = self.beautiful_soup_filter(data["snippet"])
            data["pageid"] = "https://en.wikipedia.org/wiki?curid=%d" % data["pageid"]

            if len(data["snippet"]):
                return {"text": data["snippet"], "link": data["pageid"]}
        except Exception as e:
            logging.error("Wikipedia search API error, details: %s" % e)

    def get_(self) -> dict:
        """
        Global get function
        :param text:
        :return: One item dictionary
        """
        r = self.request(self.search_text)
        return self.parser(r)