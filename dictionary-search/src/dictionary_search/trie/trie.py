from __future__ import annotations
from dictionary_search.trie.trie_node import TrieNode


class Trie:
    """
    Trie data structure for storing and searching words.

    Supports insertion, exact lookup, and deletion.
    """

    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()

    def _normalize_word(self, word: str) -> str:
        return word.strip().lower()

    def add(self, word: str) -> None:
        """
        Insert a word into the trie.
        Complexity: O(L)
        Case-insensitive
        """

        word = self._normalize_word(word)

        if not word:
            return

        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True


    def search(self, word: str) -> bool:
        """
        Exact search.
        Complexity: O(L), where L is the word length.
        Search is case-insensitive.
        """

        word = self._normalize_word(word)

        if not word:
            return False

        node = self.root

        for char in word:
            if char not in node.children:
                return False

            node = node.children[char]

        return node.is_end


    def delete(self, word: str) -> bool:
        """
        Delete a word from the trie.

        Returns True if the word was deleted,
        False if it was not found.
        Complexity: O(L), where L is the word length.
        """

        word = self._normalize_word(word)

        if not word:
            return False

        def remove(node: TrieNode, index: int) -> bool:

            if index == len(word):
                if not node.is_end:
                    return False

                node.is_end = False
                return True

            char = word[index]

            if char not in node.children:
                return False

            child = node.children[char]

            deleted = remove(child, index + 1)

            if deleted and not child.is_end and not child.children:
                del node.children[char]

            return deleted

        return remove(self.root, 0)