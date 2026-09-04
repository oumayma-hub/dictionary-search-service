from __future__ import annotations


class TrieNode:
    """
    Node in a Trie data structure.

    Each node represents a single character.
    The children dictionary stores transitions to child nodes.
    is_end indicates whether the current path forms a complete word.

    """

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end: bool = False