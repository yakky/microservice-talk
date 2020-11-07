__version__ = "0.1.0"
__author__ = "Iacopo Spalletti <i.spalletti@nephila.digital>"

import uvicorn

from book_search.app_settings import get_settings


def main():  # pragma: no cover
    """Start server with uvicorn."""
    settings = get_settings()

    uvicorn.run(
        "book_search.main:app",
        host=settings.API_IP,
        port=settings.API_PORT,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


def debug():  # pragma: no cover
    """Start server with uvicorn in debug mode."""
    settings = get_settings()

    uvicorn.run(
        "book_search.main:app",
        host=settings.API_IP,
        port=settings.API_PORT,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=True,
    )


if __name__ == "__main__":
    main()
