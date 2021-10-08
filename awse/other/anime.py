from requests import post
import logging


class AnimeSearch:
    def __init__(self, search_text) -> None:
        self.query = '''
            query ($id: Int, $page: Int, $perPage: Int, $search: String) {
                Page (page: $page, perPage: $perPage) {
                    pageInfo {
                        total
                        currentPage
                        lastPage
                        hasNextPage
                        perPage
                    }
                    media (id: $id, search: $search) {
                        id
                        type
                        description(asHtml: false)
                        isAdult
                        siteUrl
                        episodes
                        coverImage {
                            large
                            color
                        }
                        trailer {
                            id
                            site
                            thumbnail
                        }
                        title {
                            english
                            native

                        }
                    }
                }
            }
        '''
        self.variables = {
            'search': search_text,
            'page': 1,
            'perPage': 5
        }
        self.url = 'https://graphql.anilist.co'

    def request(self) -> dict:
        try:
            data = post(
                self.url,
                json={
                    'query': self.query,
                    'variables': self.variables
                }
            ).json()["data"]["Page"]

            if not data["pageInfo"]["total"]:
                raise logging.error("Anime not found")

            if data["media"]:
                x = [i for i in data["media"] if not i["isAdult"]]
                if not x: raise logging.error("All anime for audience")

                # for i in data["media"]: i["description"] = BeautifulSoup(
                #     str(i["description"]), 'lxml').text

                return data["media"]
        except Exception as e:
            logging.error("Error make request to Anilist, details: %s" % e)
