import requests
import logging

logger = logging.getLogger(__name__)

class DictionaryClient:

    """
    HTTP client for interacting with the Dictionary Search API.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url


    def search(self, word: str) -> dict:

        logger.debug(
            "Sending exact search request for %s",
            word
        )
                
        response = requests.get(
            f"{self.base_url}/search/{word}"
        )

        response.raise_for_status()

        return response.json()


    def fuzzy_search(
        self,
        word: str,
        max_distance: int
    ) -> dict:
        
        logger.debug(
            "Sending fuzzy search request for %s",
            word
        )

        response = requests.get(
            f"{self.base_url}/search/fuzzy/{word}",
            params={
                "max_distance": max_distance
            }
        )

        response.raise_for_status()

        return response.json()


    def batch_search(
        self,
        words: list[str]
    ) -> dict:
        
        logger.debug(
            "Sending batch search request for %s words",
            len(words)
        )

        response = requests.post(
            f"{self.base_url}/search/batch",
            json={
                "words": words
            }
        )

        response.raise_for_status()

        return response.json()