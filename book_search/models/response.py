from typing import List

from pydantic import BaseModel


class Author(BaseModel):
    name: str


class Tag(BaseModel):
    title: str
    slug: str


class Book(BaseModel):
    book_id: int
    title: str
    isbn13: str
    authors: List[Author]
    tags: List[Tag]
    original_publication_year: int


class BookList(BaseModel):
    results: List[Book]
    count: int
