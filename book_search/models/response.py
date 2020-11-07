from typing import List

from pydantic import BaseModel, Field


class Author(BaseModel):
    name: str


class Tag(BaseModel):
    title: str
    slug: str


class Book(BaseModel):
    book_id: int
    title: str
    isbn13: str
    authors_list: List[Author] = Field(..., alias="authors")
    tags: List[Tag]
    original_publication_year: int


class BookList(BaseModel):
    results: List[Book]
    count: int
