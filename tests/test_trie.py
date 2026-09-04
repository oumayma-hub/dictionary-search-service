import pytest

from dictionary_search.trie.trie import Trie


@pytest.fixture
def trie():
    return Trie()


# -----------------------------
# ADD + SEARCH
# -----------------------------

@pytest.mark.parametrize(
    "word",
    [
        "cat",
        "car",
        "cart",
        "dog",
        "rue de la paix",  # phrase avec espaces
    ],
)

def test_add_and_search(trie, word):
    trie.add(word)

    assert trie.search(word) is True


def test_search_non_existing(trie):
    trie.add("cat")

    assert trie.search("cow") is False


def test_search_prefix_not_word(trie):
    trie.add("cart")

    # "car" est un préfixe mais pas un mot complet
    assert trie.search("car") is False


# -----------------------------
# MULTIPLE WORDS
# -----------------------------

def test_multiple_words_independent(trie):
    words = ["cat", "car", "dog"]

    for w in words:
        trie.add(w)

    for w in words:
        assert trie.search(w) is True

    assert trie.search("cow") is False


# -----------------------------
# DELETE
# -----------------------------

def test_delete_existing_word(trie):
    trie.add("cat")

    assert trie.delete("cat") is True
    assert trie.search("cat") is False


def test_delete_non_existing_word(trie):
    trie.add("cat")

    assert trie.delete("cow") is False


def test_delete_word_keeps_others(trie):
    trie.add("cat")
    trie.add("car")

    trie.delete("cat")

    assert trie.search("cat") is False
    assert trie.search("car") is True


def test_delete_prefix_case(trie):
    trie.add("car")
    trie.add("cart")

    trie.delete("cart")

    # "car" doit rester
    assert trie.search("car") is True
    assert trie.search("cart") is False


def test_delete_word_that_is_prefix(trie):
    trie.add("car")
    trie.add("cart")

    trie.delete("car")

    # "cart" doit rester
    assert trie.search("car") is False
    assert trie.search("cart") is True


# -----------------------------
# EDGE CASES
# -----------------------------

def test_empty_string(trie):
    trie.add("")

    assert trie.search("") is False

    trie.delete("")
    assert trie.search("") is False


def test_duplicate_insert(trie):
    trie.add("cat")
    trie.add("cat")

    # ne doit pas casser
    assert trie.search("cat") is True

    trie.delete("cat")
    assert trie.search("cat") is False