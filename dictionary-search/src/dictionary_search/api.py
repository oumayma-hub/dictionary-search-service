from pathlib import Path

from fastapi import FastAPI, HTTPException
import logging

from dictionary_search.loader import load_dictionary
from dictionary_search.search import search_with_edit_distance
from dictionary_search.search import MAX_DISTANCE
from dictionary_search.models import (
    SearchResponse,
    BatchSearchRequest,
    BatchSearchResponse,
    BatchSearchResult,
    FuzzySearchResponse,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DICTIONARY_PATH = PROJECT_ROOT / "data" / "words.txt"

app = FastAPI(
    title="Dictionary Search API",
    version="1.0",
    description="REST API exposing exact and fuzzy dictionary search."
)

logger = logging.getLogger(__name__)


# Dictionary is loaded once at startup to avoid reading the file on every request.
trie = load_dictionary(DICTIONARY_PATH)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok"
    }

@app.get(
    "/search/{word}",
    response_model=SearchResponse
)
def search_word(word: str) -> SearchResponse:

    return SearchResponse(
        word=word,
        exists=trie.search(word)
    )


@app.get(
    "/search/fuzzy/{word}",
    response_model=FuzzySearchResponse
)
def fuzzy_search(
    word: str,
    max_distance: int = 1
) -> FuzzySearchResponse:
    
    # Restrict edit distance to avoid expensive searches on large dictionaries.
    if max_distance < 0 or max_distance > MAX_DISTANCE:

        logger.warning(
            "Rejected fuzzy search with invalid distance: %s",
            max_distance
        )

        raise HTTPException(
            status_code=400,
            detail="max_distance must be between 0 and 2"
        )
    
    matches = search_with_edit_distance(
        trie,
        word,
        max_distance
    )

    logger.info(
        "Fuzzy search completed: %s matches found",
        len(matches)
    )

    return FuzzySearchResponse(
        word=word,
        max_distance=max_distance,
        matches= matches
    )


@app.post(
    "/search/batch",
    response_model=BatchSearchResponse
)
def batch_search(request: BatchSearchRequest) -> BatchSearchResponse:

    results = []

    if not request.words:
        raise HTTPException(
            status_code=400,
            detail="words list cannot be empty"
        )

    for word in request.words:

        results.append(
            BatchSearchResult(
                word= word,
                exists= trie.search(word)
            )
        )
    
    logger.info(
        "Batch search completed: %s words processed",
        len(results)
    )

    return BatchSearchResponse(
        results=results
    )