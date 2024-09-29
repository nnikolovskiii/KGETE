from typing import List
from tqdm import tqdm
import logging

from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_from_general_chain import extract_triplets_from_general_chain
from app.chains.graph_types.type_extraction_from_keywords import type_extraction_from_keywords_chain
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.flows.chunks.insert_wikipedia_chunks import insert_chunks
from app.flows.graph_types.insert_general_types import insert_general_types
from app.models.models import Type, Chunk

mdb = MongoDBDatabase()

chunks: List[Chunk] = mdb.get_entries(class_type=Chunk)
if len(chunks) == 0:
    insert_chunks()

general_type_list: List[Type] = mdb.get_entries(class_type=Type, collection_name="NewType", doc_filter={'general': True})

if len(general_type_list) == 0:
    insert_general_types()

general_type_list: List[Type] = mdb.get_entries(class_type=Type, collection_name="NewType", doc_filter={'general': True})
print('\n'.join([type.value + " " + type.type for type in general_type_list]))

node_types = [str(type) for type in general_type_list if type.type == "node_type"]
rel_types = [type.value for type in general_type_list if type.type == "rel_type"]

chunks = mdb.get_entries(class_type=Chunk)

for chunk in tqdm(chunks, desc="Extracting triplets from chunks"):
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

