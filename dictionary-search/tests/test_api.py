from fastapi.testclient import TestClient

from dictionary_search.api import app


client = TestClient(app)


def test_exact_search_existing_word():

    response = client.get("/search/python")

    assert response.status_code == 200

    data = response.json()

    assert data["word"] == "python"
    assert data["exists"] is True


def test_exact_search_unknown_word():

    response = client.get("/search/java")

    assert response.status_code == 200

    data = response.json()

    assert data["exists"] is False


def test_batch_search():

    response = client.post(
        "/search/batch", 
        json={
            "words": [
                "hello",
                "python",
                "java"
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    results = data["results"]

    assert results[0]["exists"] is True
    assert results[1]["exists"] is True
    assert results[2]["exists"] is False

def test_batch_search_empty():

    response = client.post(
        "/search/batch", 
        json={
            "words": []
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert "words list cannot be empty" in data["detail"]


def test_fuzzy_search():

    response = client.get(
        "/search/fuzzy/pyhton",
        params={
            "max_distance": 2
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "python" in data["matches"]

def test_fuzzy_search_invalid_max_distance():

    response = client.get(
        "/search/fuzzy/pyhton",
        params={
            "max_distance": 5
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert "max_distance must be between 0 and 2" in data["detail"]