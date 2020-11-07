from typing import Dict

from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/", name="ping")
async def root() -> Dict[str, str]:
    """Return a static message - To be used as a canary for load balancers."""
    return {"message": "Ping"}
