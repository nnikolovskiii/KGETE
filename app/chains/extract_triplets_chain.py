from typing import Optional
import uuid

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk, Type
from app.databases.qdrant_database.qdrant_database import SearchOutput, QdrantDatabase
from app.templates.extract_triplets_template import extract_triplets_template
from pydantic import BaseModel

from app.utils.json_extraction import trim_and_load_json


class SimpleOutput(SearchOutput):
    value: str


class Triplet(BaseModel):
    id: Optional[str] = None
    head_value: str
    head_type: str
    relation: str
    tail_value: str
    tail_type: str
    chunk_id: Optional[str] = None


def extract_triplets_chain(
        chunk: Chunk,
) -> None:
    mdb = MongoDBDatabase()
    template = extract_triplets_template(
        text=chunk.context,
    )

    json_data = generic_chat_chain_json(template=template)

    if all(key in json_data for key in ["node_types", "relation_types", "triplets"]):
        node_types = json_data["node_types"]
        rel_types = json_data["relation_types"]

        for name, description in node_types.items():
            unique_id = str(uuid.uuid4())
            mdb.add_entry(Type(id=unique_id, value=name, type="node_type", description=description))

        for name, description in rel_types.items():
            unique_id = str(uuid.uuid4())
            mdb.add_entry(Type(id=unique_id, value=name, type="rel_type", description=description))

        triplets = [Triplet(**triplet) for triplet in json_data["triplets"]]
        for triplet in triplets:
            unique_id = str(uuid.uuid4())
            triplet.id = unique_id
            triplet.chunk_id = chunk.id
            mdb.add_entry(entity=triplet)

