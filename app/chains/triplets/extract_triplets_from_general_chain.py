import  uuid
from typing import List, Optional, Dict
import logging

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_chain import Triplet
from app.chains.utils.create_description_chain import create_description_chain
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk
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

        terms = set()
        terms.update([triplet.head_value for triplet in triplets])
        terms.update([triplet.tail_value for triplet in triplets])
        term_descr_pairs = create_description_chain(
            context=chunk.context,
            terms=list(terms)
        )

        for triplet in triplets:
            triplet.head_description = term_descr_pairs[triplet.head_value]
            triplet.tail_description = term_descr_pairs[triplet.tail_value]

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
            mdb.add_entry(entity=triplet, metadata={'chunk': chunk.id, 'version': '4'})

    if Database.QDRANT in databases:
        qdb = QdrantDatabase()

        for triplet in triplets:
            qdb.embedd_and_upsert_record(
                value=f"Name:{triplet.head_value}\nType:{triplet.head_type}\nDescription:{triplet.head_description}",
                collection_name="nodes",
                unique_id=triplet.id,
                metadata={"version": "4"}
            )
            qdb.embedd_and_upsert_record(
                value=f"Name:{triplet.tail_value}\nType:{triplet.tail_type}\nDescription:{triplet.tail_description}",
                collection_name="nodes",
                unique_id=triplet.id,
                metadata={"version": "4"}
            )

    return triplets
