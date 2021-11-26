from requests import get
from pydantic import BaseModel


class InfoboxContentModel(BaseModel):
    data_type: str = None
    label: str = None
    value: str = None
    wiki_order: str or int = None


class InfoboxMetaModel(BaseModel):
    data_type: str = None
    label: str = None
    value: str = None


class InfoboxModel(BaseModel):
    content: [InfoboxContentModel] = None
    meta: [InfoboxMetaModel] = None


class IconModel(BaseModel):
    Height: str or int = None
    URL: str = None
    Width: str or int = None


class AdditionalDataModel(BaseModel):
    FirstURL: str = None
    Icon: IconModel = None
    Result: str = None
    Text: str = None


class MetaModel(BaseModel):
    description: str = None
    id: str = None
    name: str = None
    src_domain: str = None


class ResultModel(BaseModel):
    Abstract: str = None
    AbstractSource: str = None
    AbstractText: str = None
    AbstractURL: str = None

    Answer: str = None
    AnswerType: str = None

    Definition: str = None
    DefinitionSource: str = None
    DefinitionURL: str = None

    Entity: str = None
    Heading: str = None

    Image: str = None
    ImageHeight: int = 0
    ImageIsLogo: bool = False
    ImageWidth: int = 0

    Infobox: InfoboxModel = None
    Redirect: str = None

    RelatedTopics: [AdditionalDataModel] = None
    Results: [AdditionalDataModel] = None

    Type: str = None
    meta: MetaModel = None


class AdditionalBlock:
    def __init__(self, search_string: str) -> None:
        self.url = "https://api.duckduckgo.com/"
        self.format = "json"
        self.search_string = search_string

    def get_json(self) -> dict or None:
        response = get(url=self.url, params={
            "q": self.search_string, "format": self.format
        }, headers={
            "Cookie": "ad=en_US"
        })
        if response.status_code >= 200 < 300:
            return response.json()

    def collected(self) -> dict or None:
        data = self.get_json()
        if data["RelatedTopics"] and data["Heading"]:
            return ResultModel(data)

    def get(self) -> dict or None:
        data = self.collected()
        if data and data.AbstractText:
            return data
