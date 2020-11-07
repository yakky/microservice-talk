from typing import List

from fastapi import APIRouter, Depends, Query
from starlette.requests import Request

from .. import models
from ..app_settings import Settings, get_settings
from ..es.search import search_es

search_router = APIRouter()


@search_router.get("/search/", response_model=models.BookListResponse, name="search")
async def search(
    request: Request,
    settings: Settings = Depends(get_settings),  # noqa: B008
    q: str = Query(None, description="Free text query string."),  # noqa: B008
    tags: List[str] = Query([], description="List of tags slugs."),  # noqa: B008
    year: int = Query(None, description="Filter by publication year."),  # noqa: B008
    size: int = Query(20, description="Number of results in the current page."),  # noqa: B008
):
    """
    Search ES data according to the provided filters.
    """
    results, total = await search_es(settings, q, year, tags, size)
    return {"results": results, "count": total}
