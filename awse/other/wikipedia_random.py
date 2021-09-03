from requests import get
from pydantic import BaseModel, ValidationError, Field
from typing import List


class ResponseWikipediaAPI(BaseModel):
    continue_: Continue = Field(None, alias='continue')
    warnings: dict = None
    query: Query = None


class Continue(BaseModel):
    excontinue: int = None
    imcontinue: str = None
    grncontinue: str = None
    continue_: str = Field(None, alias='continue')


class Query(BaseModel):
    pages: Pages = None


class Pages(BaseModel):
    pass


