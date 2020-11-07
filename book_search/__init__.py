__version__ = "0.1.0"
__author__ = "Iacopo Spalletti <i.spalletti@nephila.digital>"

import os


def main():  # pragma: no cover
    """Start server with uvicorn."""
    import uvicorn

    uvicorn.run(
        "book_search.main:app",
        host=os.getenv("API_IP", "0.0.0.0"),
        port=os.getenv("API_PORT", 5000),
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


def debug():  # pragma: no cover
    """Start server with uvicorn in debug mode."""
    import uvicorn

    uvicorn.run(
        "book_search.main:app",
        host=os.getenv("API_IP", "0.0.0.0"),
        port=os.getenv("API_PORT", 5000),
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=True,
    )
