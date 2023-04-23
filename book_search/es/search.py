from typing import List, Tuple

from elasticsearch import AsyncElasticsearch

from ..app_settings import Settings
from .documents import Book


async def search_es(
    settings: Settings, es_client: AsyncElasticsearch, q: str, year: int, tags: List[str], size: int
) -> Tuple[List[Book], int]:
    """Build the ES query and run it, returning results and total count."""
    query_dict = {"bool": {"must": []}}
    if q:
        text_query = {
            "bool": {
                "should": [
                    {"match": {"title": q}},
                    {"nested": {"path": "authors", "query": {"match": {"authors.name": q}}}},
                ]
            }
        }
        query_dict["bool"]["must"].append(text_query)
    if year:
        query_dict["bool"]["must"].append({"match": {"original_publication_year": year}})
    if tags:
        tags_query = {
            "bool": {"should": [{"nested": {"path": "tags", "query": {"match": {"tags.slug": tag}}}} for tag in tags]}
        }
        query_dict["bool"]["must"].append(tags_query)

    response = await es_client.search(index="book", query=query_dict, size=size)
    results = [row["_source"] for row in response["hits"]["hits"]]
    total = response["hits"]["total"]["value"]
    return results, total
