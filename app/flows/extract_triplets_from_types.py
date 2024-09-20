from typing import List

from app.chains.generic.models import Database
from app.chains.type_extraction_from_keywords import type_extraction_from_keywords_chain
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Type
from app.flows.types.insert_general_types import insert_general_types
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


