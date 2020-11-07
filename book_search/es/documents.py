from elasticsearch_dsl import Document, InnerDoc, Integer, Keyword, Nested, Text


class Author(InnerDoc):
    name: Text()


class Tag(InnerDoc):
    title: Text()
    slug: Keyword()


class Book(Document):
    book_id = Integer()
    isbn = Keyword()
    isbn13 = Keyword()
    authors = Nested(Author)
    original_publication_year = Integer()
    original_title = Text()
    title = Text()
    language_code = Keyword()
    small_image_url = Keyword()
    tags = Nested(Tag)

    class Index:
        name = "book"
