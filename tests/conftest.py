from functools import partial
from typing import Callable

import pytest

from book_search.es import init_es
from book_search.es.documents import Book

from .utils import load_json as load_json_func, load_json_to_es


@pytest.fixture
def settings():
    """Returns the application settings"""
    from book_search.app_settings import get_settings

    return get_settings()


@pytest.fixture
def es_init(settings):
    """Connect to ES."""

    return init_es(settings, use_async=False)


@pytest.fixture
def es_init_async(settings):
    """Connect to ES."""
    return init_es(settings, use_async=True)


@pytest.fixture
def load_json() -> Callable:
    """Return a function that loads json from data sample."""

    return load_json_func


@pytest.fixture
def load_data_to_es(es_init) -> Callable:
    """Return a function that loads json data to ES."""

    return partial(load_json_to_es, es_init)


@pytest.fixture
def load_books(load_data_to_es):
    return load_data_to_es("data.json", Book)
