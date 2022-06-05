from typing import Union

from elasticsearch import AsyncElasticsearch, Elasticsearch
from elasticsearch_dsl.connections import add_connection
from fastapi import Depends

from ..app_settings import Settings, get_settings


def init_es(settings: Settings, use_async: bool = True) -> Union[AsyncElasticsearch, Elasticsearch]:
    """Instantiate an elastic search client."""
    if use_async:
        return AsyncElasticsearch([settings.ES_HOST])
    else:
        client = Elasticsearch([settings.ES_HOST])
        add_connection("default", client)
        return client


async def get_es(
    settings=Depends(get_settings), use_async=True  # noqa: B008
) -> Union[AsyncElasticsearch, Elasticsearch]:
    """
    Get an elastic search client.

    The client connection is closed after each request.
    """
    try:
        es_client = init_es(settings, use_async=use_async)
        yield es_client
    finally:
        await es_client.close()
