import pytest
from unittest.mock import Mock, patch

from dictionary_search.client import DictionaryClient


BASE_URL = "http://127.0.0.1:8000"


def create_mock_response(json_data):
    response = Mock()
    response.json.return_value = json_data
    response.raise_for_status.return_value = None
    return response


def test_search():
    client = DictionaryClient(BASE_URL)

    mock_response = create_mock_response(
        {
            "word": "hello",
            "exists": True
        }
    )

    with patch(
        "dictionary_search.client.requests.get",
        return_value=mock_response
    ) as mock_get:

        result = client.search("hello")

    mock_get.assert_called_once_with(
        f"{BASE_URL}/search/hello"
    )

    assert result["word"] == "hello"
    assert result["exists"] is True


def test_search_word_not_found():
    client = DictionaryClient(BASE_URL)

    mock_response = create_mock_response(
        {
            "word": "unknown",
            "exists": False
        }
    )

    with patch(
        "dictionary_search.client.requests.get",
        return_value=mock_response
    ) as mock_get:

        result = client.search("unknown")

    mock_get.assert_called_once_with(
        f"{BASE_URL}/search/unknown"
    )

    assert result["exists"] is False


def test_fuzzy_search():
    client = DictionaryClient(BASE_URL)

    mock_response = create_mock_response(
        {
            "word": "helo",
            "matches": ["hello"],
            "max_distance": 1
        }
    )

    with patch(
        "dictionary_search.client.requests.get",
        return_value=mock_response
    ) as mock_get:

        result = client.fuzzy_search(
            "helo",
            max_distance=1
        )

    mock_get.assert_called_once_with(
        f"{BASE_URL}/search/fuzzy/helo",
        params={
            "max_distance": 1
        }
    )

    assert "hello" in result["matches"]


def test_batch_search():
    client = DictionaryClient(BASE_URL)

    mock_response = create_mock_response(
        {
            "results": [
                {"word": "hello", "exists": True},
                {"word": "word", "exists": False}
            ]
        }
    )

    with patch(
        "dictionary_search.client.requests.post",
        return_value=mock_response
    ) as mock_post:

        result = client.batch_search(
            [
                "hello",
                "word"
            ]
        )

    mock_post.assert_called_once_with(
        f"{BASE_URL}/search/batch",
        json={
            "words": [
                "hello",
                "word"
            ]
        }
    )

    assert result["results"][0]["exists"] is True
    assert result["results"][1]["exists"] is False


def test_http_error_is_propagated():
    client = DictionaryClient(BASE_URL)

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception(
        "HTTP error"
    )

    with patch(
        "dictionary_search.client.requests.get",
        return_value=mock_response
    ):
        with pytest.raises(Exception, match="HTTP error"):
            client.search("hello")