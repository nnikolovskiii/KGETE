import  uuid
from typing import List, Optional, Dict
import logging

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk, Type
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from app.templates.extract_triplets_with_general_types import extract_triplets_from_general_template


def extract_triplets_from_general_chain(
        chunk: Chunk,
        node_types: List[str],
        rel_types: List[str],
        databases: Optional[List[Database]] = None
) -> List[Triplet]:
    template = extract_triplets_from_general_template(
        text=chunk.context,
        node_types=node_types,
        rel_types=rel_types
    )

    json_data = generic_chat_chain_json(template=template)
    triplets: List[Triplet] = []

    if "triplets" in json_data:
        triplets = [Triplet(**triplet) for triplet in json_data["triplets"]]

    if "descriptions" in json_data:
        descr_dict = json_data["descriptions"]

        for triplet in triplets:
            head_value = triplet.head_value
            tail_value = triplet.tail_value
            if head_value in list(descr_dict.keys()):
                triplet.head_description = descr_dict[head_value]
            else:
                logging.warning(f"No description found for triplet: {triplet}, head_value: {head_value}")

            if tail_value in list(descr_dict.keys()):
                triplet.tail_description = descr_dict[tail_value]
            else:
                logging.warning(f"No description found for triplet: {triplet}, head_value: {tail_value}")


    # databases
    if not databases:
        return triplets

    if Database.MONGO in databases:
        mdb = MongoDBDatabase()

        for triplet in triplets:
            unique_id = str(uuid.uuid4())
            triplet.id = unique_id
            triplet.chunk_id = chunk.id
            mdb.add_entry(entity=triplet, metadata={'chunk': chunk.id, 'version': '3'})

    if Database.QDRANT in databases:
        qdb = QdrantDatabase()

        for triplet in triplets:
            qdb.embedd_and_upsert_record(
                value=f"{triplet.head_value}: {triplet.head_description}",
                collection_name="triplets",
                unique_id=triplet.id,
                metadata={"version": "3"}
            )

    return triplets
