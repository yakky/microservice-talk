import json
import os
from typing import Any, Dict, Type

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Document as BaseDocument, Index


def load_json(json_file: str) -> Any:
    """Loads json from data sample."""
    local_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(local_path, "data", json_file)) as jfile:
        return json.load(jfile)


def load_json_to_es(es: Elasticsearch, json_file: str, EsDocument: Type[BaseDocument]) -> Dict[str, str]:  # noqa: N803
    """Load a ES json fixture on ES patching the index according to the given group."""

    def stream_data(index, data):
        for row in data:
            row.update(
                {
                    "_index": index,
                    "_id": row["book_id"],
                }
            )
            yield row

    json_data = load_json(json_file)
    index_name = EsDocument.Index.name
    Index(index_name).delete(ignore=404)
    EsDocument.init()
    bulk(es, stream_data(index_name, json_data))
    Index(index_name).refresh()
    return json_data
