import  uuid
from typing import List, Optional

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk, Type
from app.templates.combine_triplets_template import combine_triplets_template
from app.templates.extract_triplets_with_general_types import extract_triplets_from_general_template
from pydantic import BaseModel


class ReducedNode(BaseModel):
    id: str
    name: str
    sub_node_names: List[str]


def extract_triplets_from_general_chain(
        triplets: List[Triplet],
        contexts: List[str],
        databases: Optional[List[Database]] = None
) -> List[ReducedNode]:
    template = combine_triplets_template(
        triplets= [str(triplet) for triplet in triplets],
        contexts= contexts,
    )

    json_data = generic_chat_chain_json(template=template)

    reduced_nodes: List[ReducedNode] = []

    if "groups" in json_data:
        reduced_nodes = [ReducedNode(
            id=str(uuid.uuid4()),
            name=reduced_node["name"],
            sub_node_names=reduced_node["sub_nodes"],
        ) for reduced_node in json_data["groups"]]

        # databases
        if not databases:
            return reduced_nodes

        if Database.MONGO in databases:
            mdb = MongoDBDatabase()

            for reduced_node in reduced_nodes:
                mdb.add_entry(entity=reduced_node)

    return reduced_nodes
