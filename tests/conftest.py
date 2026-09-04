import pytest
from logging_config import setup_logging


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    setup_logging()