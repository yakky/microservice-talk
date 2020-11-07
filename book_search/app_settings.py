import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME = "Book Search"
    API_V1_STR = "/api/v1"

    ES_HOST = "127.0.0.1:9200"
    """
    .. _ES_HOST:

    ElasticSearch hosts
    """
    BACKEND_CORS_ORIGINS: str = ".*"

    class Config:
        case_sensitive = False
        env_file = Path(os.getcwd()) / ".env"


@lru_cache()
def get_settings() -> BaseSettings:
    """
    Get settings instance.

    Cached via lru_cache.
    """
    return Settings()
