import typer

from book_search.app_settings import Settings
from book_search.es import init_es
from book_search.es.documents import Book
from tests.utils import load_json_to_es


def main(path: str):
    es = init_es(Settings(), use_async=False)
    load_json_to_es(es, path, Book)


if __name__ == "__main__":
    typer.run(main)
