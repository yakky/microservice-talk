from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api import api_router, root_router
from .app_settings import get_settings  # noqa

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(root_router)
app.include_router(api_router, prefix=settings.API_V1_STR)
