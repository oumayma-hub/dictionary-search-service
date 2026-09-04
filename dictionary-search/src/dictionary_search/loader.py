from pathlib import Path
from dictionary_search.trie.trie import Trie
import logging

logger = logging.getLogger(__name__)


def load_dictionary(file_path: Path) -> Trie:
    """
    Load words from a file and build a Trie.
    """
    
    logger.info(
        "Loading dictionary: %s",
        file_path
    )

    if not file_path.exists():
        logger.exception(
            "Dictionary file missing: %s",
            file_path
        )

        raise FileNotFoundError(
            f"Dictionary file not found: {file_path}"
        )

    trie = Trie()
    count: int = 0

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            word = line.strip()

            if word:
                trie.add(word)
                count += 1

    logger.info(
        "Dictionary loaded successfully. Loaded %s words",
        count
    )   

    return trie