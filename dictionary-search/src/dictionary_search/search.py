"""
Implements OCR-tolerant search algorithms.

Includes:
- substitution-only search (baseline)
- full edit-distance search using insertion, deletion, and substitution.
"""
from dictionary_search.trie.trie_node import TrieNode

import logging


logger = logging.getLogger(__name__)
MAX_DISTANCE = 5


def _normalize_word(word: str) -> str:
    return word.strip().lower()


def search_with_substitution(
    trie,
    word: str,
    max_errors: int
) -> list[str]:
    """
    Search words allowing substitution errors only.
    """
    
    _validate_error_limit(max_errors)
    
    word = _normalize_word(word)

    results = []


    def dfs(
        node: TrieNode,
        index: int,
        errors: int,
        current: str
    ) -> None:

        if errors > max_errors:
            return


        if index == len(word):

            if node.is_end:
                results.append(current)

            return


        for char, child in node.children.items():

            new_errors = errors + (
                char != word[index]
            )

            dfs(
                child,
                index + 1,
                new_errors,
                current + char
            )


    dfs(
        trie.root,
        0,
        0,
        ""
    )

    return results


def _validate_error_limit(max_distance: int) -> None:
    """
    Validate maximum edit distance.

    Limits the search depth to avoid expensive computations.
    """
    if max_distance < 0 or max_distance > MAX_DISTANCE:
        raise ValueError(
            f"max_distance must be between 0 and {MAX_DISTANCE}"
        )


def search_with_edit_distance(
    trie,
    word: str,
    max_distance: int
) -> list[str]:
    """
    Full edit-distance search (insertion + deletion + substitution)
    """
    
    _validate_error_limit(max_distance)
    
    word = _normalize_word(word)

    logger.debug(
        "Starting fuzzy search: word=%s distance=%s",
        word,
        max_distance
    )

    results = []


    initial_row = list(range(len(word) + 1))


    def dfs(
        node,
        prefix,
        previous_row
    ) -> None:

        for char, child in node.children.items():

            current_row = [
                previous_row[0] + 1
            ]


            for i in range(1, len(word) + 1):

                insertion = (
                    current_row[i - 1] + 1
                )

                deletion = (
                    previous_row[i] + 1
                )

                substitution = (
                    previous_row[i - 1]
                    + (word[i - 1] != char)
                )


                current_row.append(
                    min(
                        insertion,
                        deletion,
                        substitution
                    )
                )


            distance = current_row[-1]


            if distance <= max_distance and child.is_end:
                results.append(
                    prefix + char
                )


            # pruning
            if min(current_row) <= max_distance:
                dfs(
                    child,
                    prefix + char,
                    current_row
                )


    dfs(
        trie.root,
        "",
        initial_row
    )

    logger.debug(
        "Fuzzy search finished: %s results",
        len(results)
    )


    return results