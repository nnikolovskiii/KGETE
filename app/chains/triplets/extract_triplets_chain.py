from typing import Optional
import uuid

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import SearchOutput
from app.models.models import Chunk, Type
from app.templates.triplets.extract_triplets_template import extract_triplets_template
from pydantic import BaseModel


class SimpleOutput(SearchOutput):
    value: str


class Node(BaseModel):
    id: Optional[str] = None
    value: str
    type: str
    description: str
    triplet_id: str
    parent_node: Optional[str] = None
    latest: Optional[bool] = False

    class Config:
        frozen = True

    def __str__(self):
        return f"""{self.value}, {self.type}, {self.description}"""

    def __hash__(self):
        return hash((self.value, self.type, self.description))

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.value, self.type, self.description) == (other.value, other.type, other.description)
        return False


class Triplet(BaseModel):
    id: Optional[str] = None
    head_value: str
    head_type: str
    relation: str
    tail_value: str
    tail_type: str
    chunk_id: Optional[str] = None

    def __str__(self) -> str:
        return f"({self.head_value}: {self.head_type}) - [{self.relation}] → ({self.tail_value}: {self.tail_type})"

    def str_with_description(self) -> str:
        head = f"Node{{value:{self.head_value}, type:{self.head_type}, description:{self.head_description}}}"
        tail = f"Node{{value:{self.tail_value}, type:{self.tail_type}, description:{self.tail_description}}}"
        return head + "\n" + tail


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

