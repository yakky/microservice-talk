from typing import List

from fastapi import APIRouter, Query
from starlette.requests import Request

from .. import models
from ..es import init_es

search_router = APIRouter()


@search_router.get("/search/", response_model=models.BookListResponse, name="search")
async def search(
    request: Request,
    q: str = Query(None, description="Free text query string."),  # noqa: B008
    tags: List[str] = Query([], description="List of Topics UUID."),  # noqa: B008
    year: int = Query(None, description="Filter by publication year."),  # noqa: B008
    size: int = Query(20, description="Number of returned results."),  # noqa: B008
):
    """
    Search ES data according to the provided filters.
    """
    client = init_es(use_async=True)
    query_dict = {"query": {"bool": {"must": []}}}
    if q:
        text_query = {
            "bool": {
                "should": [
                    {"match": {"title": q}},
                    {"nested": {"path": "authors", "query": {"match": {"authors.name": q}}}},
                ]
            }
        }
        query_dict["query"]["bool"]["must"].append(text_query)
    if year:
        query_dict["query"]["bool"]["must"].append({"match": {"original_publication_year": year}})
    if tags:
        tags_query = {
            "bool": {"should": [{"nested": {"path": "tags", "query": {"match": {"tags.slug": tag}}}} for tag in tags]}
        }
        query_dict["query"]["bool"]["must"].append(tags_query)

    response = await client.search(index="book", body=query_dict, size=size)
    results = [row["_source"] for row in response["hits"]["hits"]]
    total = response["hits"]["total"]["value"]
    await client.close()
    return {"results": results, "count": total}
