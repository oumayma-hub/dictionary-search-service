import pytest
from dictionary_search.trie.trie import Trie
from dictionary_search.search import (
    search_with_substitution,
    search_with_edit_distance,
)


def build_trie():
    trie = Trie()

    words = [
        "cat",
        "car",
        "cart",
        "dog",
        "door",
        "python",
        "house",
    ]

    for word in words:
        trie.add(word)

    return trie


# -----------------------------
# Substitution tests
# -----------------------------

def test_substitution_one_error():
    trie = build_trie()

    result = search_with_substitution(
        trie,
        "bat",
        1
    )

    assert "cat" in result


def test_substitution_too_many_errors():
    trie = build_trie()

    result = search_with_substitution(
        trie,
        "xyz",
        1
    )

    assert result == []


def test_substitution_exact_match():
    trie = build_trie()

    result = search_with_substitution(
        trie,
        "dog",
        0
    )

    assert result == ["dog"]


# -----------------------------
# Levenshtein tests
# -----------------------------
# substitution
# -----------------------------

def test_edit_distance_substitution():
    trie = build_trie()

    result = search_with_edit_distance(
        trie,
        "cot",
        1
    )

    assert "cat" in result


# -----------------------------
# insertion tests
# -----------------------------

def test_edit_distance_insertion():
    trie = build_trie()

    result = search_with_edit_distance(
        trie,
        "cats",
        1
    )

    assert "cat" in result


def test_edit_distance_insertion_at_beginning():
    trie = build_trie()

    result = search_with_edit_distance(
        trie,
        "scat",
        1
    )

    assert "cat" in result


# -----------------------------
# deletion tests
# -----------------------------

def test_edit_distance_deletion():
    trie = build_trie()

    result = search_with_edit_distance(
        trie,
        "at",
        1
    )

    assert "cat" in result


def test_edit_distance_deletion_middle():
    trie = build_trie()

    result = search_with_edit_distance(
        trie,
        "ct",
        1
    )

    assert "cat" in result


# -----------------------------
# Combined errors
# -----------------------------

def test_edit_distance_multiple_operations():
    trie = build_trie()

    # cat -> coat
    # insertion of 'o'
    result = search_with_edit_distance(
        trie,
        "coat",
        1
    )

    assert "cat" in result


def test_edit_distance_no_match():
    trie = build_trie()

    result = search_with_edit_distance(
        trie,
        "zzzz",
        2
    )

    assert result == []


# -----------------------------
# Exact search through edit distance
# -----------------------------

def test_edit_distance_zero():
    trie = build_trie()

    result = search_with_edit_distance(
        trie,
        "python",
        0
    )

    assert result == ["python"]