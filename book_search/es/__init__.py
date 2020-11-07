from typing import Union

from elasticsearch import AsyncElasticsearch, Elasticsearch
from elasticsearch_dsl.connections import add_connection

from ..app_settings import Settings


def init_es(settings: Settings, use_async: bool = True) -> Union[AsyncElasticsearch, Elasticsearch]:
    """Instantiate an elastic search client."""
    if use_async:
        return AsyncElasticsearch([settings.ES_HOST])
    else:
        client = Elasticsearch([settings.ES_HOST])
        add_connection("default", client)
        return client
