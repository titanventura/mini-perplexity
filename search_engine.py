from typing import Annotated

from fastapi import Depends
from googleapiclient.discovery import build

from config import Settings, get_settings
from utils import async_wrap


def get_search_engine(settings: Annotated[Settings, Depends(get_settings)]):
    return SearchEngine(settings.search_api_key, settings.search_engine_id)


class SearchEngine:
    def __init__(self, google_api_key: str, google_search_engine_id: str):
        self.service = build("customsearch", "v1", developerKey=google_api_key)
        self.search_engine_id = google_search_engine_id

    @async_wrap
    def search(self, term: str, **kwargs) -> list[dict]:
        res = self.service.cse().list(q=term, cx=self.search_engine_id, **kwargs).execute()
        return res['items']