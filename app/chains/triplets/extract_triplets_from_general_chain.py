import  uuid
from typing import List, Optional

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.models.models import Chunk
from app.templates.triplets.extract_triplets_with_general_types import extract_triplets_from_general_template


def extract_triplets_from_general_chain(
        chunk: Chunk,
        node_types: List[str],
        rel_types: List[str],
        databases: Optional[List[Database]] = None
) -> List[Triplet]:
    template = extract_triplets_from_general_template(
        text=chunk.context,
        # node_types=node_types,
        rel_types=rel_types
    )

    json_data = generic_chat_chain_json(template=template)
    triplets: List[Triplet] = []

    if "triplets" in json_data:
        triplets = [Triplet(**triplet) for triplet in json_data["triplets"]]

    else:
        raise Exception("Badly generated response from llm. No key triplets.")

    # databases
    if not databases:
        return triplets

    if Database.MONGO in databases:
        mdb = MongoDBDatabase()

        for triplet in triplets:
            unique_id = str(uuid.uuid4())
            triplet.id = unique_id
            triplet.chunk_id = chunk.id
            mdb.add_entry(entity=triplet, collection_name="NewTriplet")

    return triplets
