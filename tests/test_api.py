from urllib.parse import urlencode

import httpx
import pytest

from book_search.main import app


@pytest.mark.asyncio
async def test_search_basic(load_books):
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        url = app.url_path_for("search")
        params = urlencode({"q": "Susan Collins"})
        response = await client.get(f"{url}?{params}")
        assert response.status_code == 200
        data = response.json()
        assert data["results"]
        assert data["count"] == 3
        assert [row["book_id"] for row in data["results"]] == [1, 17, 20]
        for row in data["results"]:
            assert row["title"]
            assert row["isbn13"]


@pytest.mark.asyncio
async def test_search_year(load_books):
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        url = app.url_path_for("search")
        params = urlencode({"year": 2008})
        response = await client.get(f"{url}?{params}")
        assert response.status_code == 200
        data = response.json()
        assert data["results"]
        assert data["count"] == 4
        assert [row["book_id"] for row in data["results"]] == [1, 56, 73, 88]
        for row in data["results"]:
            assert row["title"]
            assert row["isbn13"]


@pytest.mark.asyncio
async def test_search_tags(load_books):
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        url = app.url_path_for("search")
        params = urlencode({"tags": ["between-film", "address-year"]})
        response = await client.get(f"{url}?{params}")
        assert response.status_code == 200
        data = response.json()
        assert data["results"]
        assert data["count"] == 4
        assert [row["book_id"] for row in data["results"]] == [1, 2, 67, 90]
        for row in data["results"]:
            assert row["title"]
            assert row["isbn13"]


@pytest.mark.asyncio
async def test_ping():
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        url = app.url_path_for("ping")
        response = await client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Ping"
