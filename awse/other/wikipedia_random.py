import logging
import re
from json import dumps
from json.decoder import JSONDecodeError
from time import time

import requests.exceptions as requests_exceptions
from bs4 import BeautifulSoup
from requests import get


class WikiRandomGet:
    def __init__(self) -> None:
        """
        Init request params
        :param search_text: Search text
        :return: None
        """
        self.request_params = {
            "format": "json",
            "action": "query",
            "generator": "random",
            "grnnamespace": 0,
            "prop": "extracts",
            "rvprop": "content",
            "exintro": None,
            "explaintext": None,
            "redirects": 1,
            "grnlimit": 1,
        }
        self.bf_mode = True
        self.remove_tags_ = ["span"]

    def request(self) -> dict or None:
        """
        Make request and return data
        :return: raw data from wikipedia api
        """
        try:
            response = get(
                "https://en.wikipedia.org/w/api.php",
                params=self.request_params,
            )
            return response.json()["query"]["pages"], response.status_code

        except requests_exceptions.ConnectionError as e:
            logging.error("Error connetion to Wikipedia API, details: %s" % e)
        except requests_exceptions.ConnectTimeout as e:
            logging.error("Wikipedia API does not respond for too long, details: %s" % e)
        except requests_exceptions.HTTPError as e:
            logging.error("There was an error connecting to Wikipedia API, details: %s" % e)
        except JSONDecodeError as e:
            logging.error(
                "An error occurred while processing the JSON response from the " +
                "Wikipedia API, details: %s" % e
            )
        except Exception as e:
            logging.error(
                "An error occurred while trying to connect to the Wikipedia API " +
                "and retrieve information. Details: %s" % e
            )

    def select_page(self, data) -> dict or None:
        """
        We choose random data
        :return: random item from list pages
        """
        try:
            keys = [i for i in data]
            return data[keys[0]]

        except Exception as e:
            logging.error(
                "An error occurred while selecting an item from " +
                "the Wikipedia API response, details: %s" % e
            )

    def remove_comment(self, text) -> str:
        """
        Remove all HTML comments
        :return: Filtered text
        """
        return re.sub(
            r"(<!--.*?-->)", "", text, flags=re.DOTALL
        )

    def select_first(self, text) -> str:
        """
        Choose the first paragraph from the resulting text
        :return: Selected fragment
        """
        return text.split("\n\n")[0]

    def remove_tags(self, text) -> str:
        """
        Cleaning up unnecessary tags
        :return: Filtered text
        """
        for tag in self.remove_tags_:
            text = re.sub(
                r"<%s.*?</%s>" % (tag, tag), "", text
            )
        return text

    def remove_tags_params(self, text) -> str:
        """
        Delete all parameters in tags, classes, identifiers, etc.
        :return: Filtered text
        """
        return re.sub(r"(<[^/].*?)\s.*?>", r"\1>", text)

    def adapt_transfer_text(self, text) -> str:
        """
        Adaptation of transfer under HTML
        :return: Adapted text
        """
        return text.replace("\n", "</br>")

    def beautiful_soup_filter(self, text) -> str:
        return BeautifulSoup(text, 'lxml').text

    def filters(self, text) -> str:
        """
        Combining filters into one function for easy calling
        :return: Filtered text
        """
        if not self.bf_mode:
            text = self.remove_tags(text)
            text = self.remove_tags_params(text)
            text = self.adapt_transfer_text(text)
        text = self.beautiful_soup_filter(text)

        return text

    def get_(self) -> dict:
        """
        Issuance function
        :return: HTML text
        """
        start_order = time()

        for _ in range(10):
            data, code = self.request()
            if code >= 200 < 300:
                start_ = time()
                page = self.select_page(data)
                page_id = page["pageid"]
                extract = self.remove_comment(page["extract"])

                # Post edit
                first_el = self.select_first(extract)
                filter_ = self.filters(first_el)

                if len(filter_) > 250:
                    return dumps({
                        "text": filter_, "process_time": (time() - start_),
                        "full_order_time": (time() - start_order),
                        "link": "https://en.wikipedia.org/wiki?curid=%d" % page_id,
                    })
