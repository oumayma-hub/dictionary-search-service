from pydantic import BaseModel


class SearchResponse(BaseModel):
    word: str
    exists: bool


class BatchSearchRequest(BaseModel):
    words: list[str]


class BatchSearchResult(BaseModel):
    word: str
    exists: bool


class BatchSearchResponse(BaseModel):
    results: list[BatchSearchResult]


class FuzzySearchResponse(BaseModel):
    word: str
    max_distance: int
    matches: list[str]