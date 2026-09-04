# Dictionary Search Service

A dictionary search service based on a Trie data structure.

The application provides:

- Exact word search
- Batch word search
- Fuzzy search using edit distance
- REST API
- Python client
- CLI interface
- Automated tests


## Project structure

```text
dictionary-search/
├── src/
│   └── dictionary_search/
│       ├── api.py               # FastAPI endpoints
│       ├── client.py            # Python HTTP client
│       ├── loader.py            # Dictionary loader
│       ├── models.py            # API contracts
│       ├── search.py            # Exact + fuzzy search logic
│       └── trie/
│           ├── trie.py          # Trie implementation
│           └── trie_node.py     # Trie node structure
│
├── data/
│   └── words.txt
│
├── tests/
│   ├── conftest.py
│   ├── test_trie.py
│   ├── test_search.py
│   ├── test_api.py
│   └── test_client.py
│
├── logging_config.py
├── main.py                      # CLI entrypoint
├── requirements.txt
├── pyproject.toml  
├── pytest.ini 
└── README.md
```


# Installation

## Requirements

- Python >= 3.10


## Create virtual environment 

### Windows (PowerShell)

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### Windows PowerShell note

If you encounter an execution‑policy error when activating the environment,
you can temporarily allow script execution for the current session:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Deactivate

```bash
deactivate
```


## Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```


# Running tests

Run the complete test suite:

```bash
pytest -v
```

The test suite includes:

- Trie unit tests
- Search algorithm tests
- API tests
- Client tests


# Running the API

Start the FastAPI server:

```bash
uvicorn dictionary_search.api:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```


# Using the CLI client

The CLI communicates with the running API.

## Exact search

Command:

```bash
python main.py search python
```

Example response:

```json
{
    "word": "python",
    "exists": true
}
```


## Fuzzy search

Search with edit distance:

```bash
python main.py fuzzy pyhton --distance 2
```

Example response:

```json
{
    "word": "pyhton",
    "matches": [
        "python"
    ],
    "max_distance": 2
}
```


## Batch search

Search multiple words:

```bash
python main.py batch hello python java
```

Example response:

```json
{
    "results": [
        {
            "word": "hello",
            "exists": true
        },
        {
            "word": "python",
            "exists": true
        },
        {
            "word": "java",
            "exists": false
        }
    ]
}
```


# API Endpoints & Contracts

The API exposes the following endpoints.

## Health check

### Request

GET /health

### Response

{
    "status": "ok"
}


---

## Exact word search

Checks whether a word exists in the dictionary.

### Request

GET /search/{word}

Example:

GET /search/python

### Response

{
    "word": "python",
    "exists": true
}

### Response fields

| Field | Type | Description |
|------|------|-------------|
| word | string | The searched word |
| exists | boolean | Whether the word exists in the dictionary |


---

## Fuzzy search

Searches for words using edit distance.

The maximum allowed distance is limited to 2 to prevent excessive processing time.

### Request

GET /search/fuzzy/{word}?max_distance={distance}

Example:

GET /search/fuzzy/pyhton?max_distance=1

### Response

{
    "word": "pyhton",
    "max_distance": 1,
    "matches": [
        "python"
    ]
}

### Response fields

| Field | Type | Description |
|------|------|-------------|
| word | string | The searched word |
| max_distance | integer | Maximum allowed edit distance |
| matches | array[string] | Words matching the search criteria |


### Error response

If the requested distance is invalid:

Request:

GET /search/fuzzy/python?max_distance=5

Response:

{
    "detail": "max_distance must be between 0 and 2"
}

Status code:

400 Bad Request


---

## Batch word search

Searches multiple words in a single request.

### Request

POST /batch/search

Body:

{
    "words": [
        "hello",
        "python",
        "java"
    ]
}


### Response

{
    "results": [
        {
            "word": "hello",
            "exists": true
        },
        {
            "word": "python",
            "exists": true
        },
        {
            "word": "java",
            "exists": false
        }
    ]
}


### Request fields

| Field | Type | Description |
|------|------|-------------|
| words | array[string] | List of words to search |


### Response fields

| Field | Type | Description |
|------|------|-------------|
| results | array | Search result for each requested word |
| results[].word | string | The searched word |
| results[].exists | boolean | Whether the word exists in the dictionary |


---

# Logging

For this case study, a centralized logging configuration was chosen to simplify debugging and execution tracking.

All application components (API, client, search algorithms, dictionary loading, and tests) write their logs to a single log file. This makes it easier to follow the complete execution flow across the different processes involved in the application.

The logging configuration records different severity levels:

- DEBUG: detailed information useful during development and troubleshooting.
- INFO: normal application flow (startup, requests, completed operations).
- WARNING: unexpected but recoverable situations (for example invalid user inputs).
- ERROR: failures requiring attention.

In a production environment, logging would typically be handled differently, with separate configurations depending on the component, structured logs (for example JSON format), log rotation, and centralized log collection. The current approach was selected to keep the case study simple while maintaining visibility during development and testing.

# Design choices

The choices made in this implementation are adapted to the scope of this exercise. A production-scale system would require additional considerations such as scalability, deployment, monitoring, and distributed architecture, which would be addressed in the second part of the exercise.

The project separates responsibilities:

- Trie implementation handles dictionary storage and exact lookup.
- Search layer handles fuzzy search algorithms.
- API layer exposes HTTP endpoints and validates API inputs.
- Client layer communicates with the API.
- CLI provides a simple user interface.

Trie insertion and exact search have O(L) complexity, where L is the length of the searched word.

Dictionary entries are normalized to lowercase to provide consistent search behavior across all components.

Fuzzy search uses trie traversal combined with dynamic programming and pruning to avoid scanning the entire dictionary.

The batch lookup endpoint uses exact dictionary lookup, matching the behavior of the standard search endpoint.

Fuzzy search is exposed through a dedicated endpoint because edit-distance search has a higher computational cost and a different use case. A batch fuzzy search capability could be added in the future if required.

The API is intentionally started separately from the client to keep components independent, easier to test, and closer to a real client-server architecture.

The dictionary is loaded once when the API starts, avoiding repeated file reads during requests.

The substitution-only implementation is kept as a baseline for comparison. The API uses the full edit-distance implementation, which supports insertion, deletion, and substitution errors.
