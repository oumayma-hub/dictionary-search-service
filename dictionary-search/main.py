"""
CLI entry point for the dictionary search client.
"""

import argparse
import logging

from dictionary_search.client import DictionaryClient
from logging_config import setup_logging

API_URL = "http://127.0.0.1:8000"

setup_logging()
logger = logging.getLogger(__name__)



def main():

    parser = argparse.ArgumentParser(
        description="Dictionary API client"
    )

    parser.add_argument(
        "operation",
        choices=[
            "search",
            "fuzzy",
            "batch"
        ],
        help="Search operation to execute"
    )

    parser.add_argument(
        "words",
        nargs="+",
        help="Word(s) to search"
    )

    parser.add_argument(
        "--distance",
        type=int,
        default=1,
        help="Maximum edit distance for fuzzy search"
    )

    args = parser.parse_args()

    client = DictionaryClient(API_URL)

    try:

        if args.operation == "search":

            result = client.search(
                args.words[0]
            )

        elif args.operation == "fuzzy":

            result = client.fuzzy_search(
                args.words[0],
                args.distance
            )

        elif args.operation == "batch":

            result = client.batch_search(
                args.words
            )

        print(result)

    except Exception as error:

        print(
            f"Error while calling dictionary API: {error}"
        )
        print(
            "Make sure the API is running:"
        )
        print(
            "uvicorn dictionary_search.api:app"
        )


if __name__ == "__main__":
    main()