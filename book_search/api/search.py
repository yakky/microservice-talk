from __future__ import annotations

from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends, Query
from starlette.requests import Request

from .. import models
from ..app_settings import Settings, get_settings
from ..es import get_es
from ..es.search import search_es

search_router = APIRouter()


@search_router.get("/search/", name="search")
async def search(
    request: Request,
    settings: Settings = Depends(get_settings),
    es_client: AsyncElasticsearch = Depends(get_es),
    tags: Annotated[list[str] | None, Query(description="List of tags slugs.")] = None,
    year: Annotated[int | None, Query(description="Filter by publication year.")] = None,
    size: Annotated[int, Query(description="Number of results in the current page.")] = 20,
    q: Annotated[str | None, Query(description="Free text query string.")] = None,
) -> models.BookListResponse:
    """
    Search ES data according to the provided filters.
    """
    tags = tags or []
    results, total = await search_es(settings, es_client, q, year, tags, size)
    return models.BookListResponse(results=results, count=total)
