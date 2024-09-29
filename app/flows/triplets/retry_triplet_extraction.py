import logging
from typing import Set, List

from tqdm import tqdm

from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_from_general_chain import extract_triplets_from_general_chain
from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.models.models import Chunk, Type

mdb = MongoDBDatabase()

chunks = mdb.get_entries(class_type=Chunk)

while True:
    triplets = mdb.get_entries(class_type=Triplet, collection_name="NewTriplet")
    existing_chunk_ids: Set[str] = set()
    [existing_chunk_ids.add(triplet.chunk_id) for triplet in triplets]
    unprocessed_chunks: List[Chunk] = [chunk for chunk in chunks if chunk.id not in existing_chunk_ids]

    if len(unprocessed_chunks) == 0:
        break

    logging.info(f"There are {len(unprocessed_chunks)} unprocessed chunks for triple extraction.")

    general_type_list: List[Type] = mdb.get_entries(class_type=Type, doc_filter={'general': True})

    node_types = [type.value for type in general_type_list if type.type == "node_type"]
    rel_types = [type.value for type in general_type_list if type.type == "rel_type"]

    for chunk in tqdm(unprocessed_chunks, desc="Extracting triplets"):
        try:
            extract_triplets_from_general_chain(
                chunk=chunk,
                node_types=node_types,
                rel_types=rel_types,
                databases=[Database.MONGO]
            )
        except Exception as e:
            logging.warning(f"Chunk isn't processed {chunk.id}, exception {e}")
            continue
