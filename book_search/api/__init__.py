from fastapi import APIRouter

from .root import root_router  # noqa: F401
from .search import search_router  # noqa: F401

api_router = APIRouter()
api_router.include_router(search_router)
