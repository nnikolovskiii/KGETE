from typing import List
from tqdm import tqdm

from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_from_general_chain import extract_triplets_from_general_chain
from app.chains.type_extraction_from_keywords import type_extraction_from_keywords_chain
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Type, Chunk
from app.flows.graph_types.insert_general_types import insert_general_types
from app.ml_algorithms.tf_idf import get_context_from_top_keywords

mdb = MongoDBDatabase()

general_type_list: List[Type] = mdb.get_entries(class_type=Type, doc_filter={'general': True})
if len(general_type_list) == 0:
    insert_general_types()

    context, keywords = get_context_from_top_keywords()
    type_extraction_from_keywords_chain(
        context=context,
        keywords=keywords,
        databases=[Database.MONGO, Database.QDRANT]
    )

    general_type_list: List[Type] = mdb.get_entries(class_type=Type, doc_filter={'general': True})
    print(len(general_type_list))

node_types = [type.value for type in general_type_list if type.type == "node_type"]
rel_types = [type.value for type in general_type_list if type.type == "rel_type"]

chunks = mdb.get_entries(class_type=Chunk)

for chunk in tqdm(chunks[70+45+68+51:], desc="Extracting triplets from chunks"):
    extract_triplets_from_general_chain(
        chunk = chunk,
        node_types = node_types,
        rel_types=rel_types,
        databases=[Database.MONGO]
    )
