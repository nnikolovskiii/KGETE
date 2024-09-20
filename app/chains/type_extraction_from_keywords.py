import uuid
from typing import List, Optional
import logging

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.chains.generic.models import Database
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Type
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from app.templates.type_extraction_from_keywords import type_extraction_from_keywords_template


def type_extraction_from_keywords_chain(
        context: str,
        keywords: List[str],
        databases: Optional[List[Database]] = None
) -> List[Type]:
    # chain
    template = type_extraction_from_keywords_template(context=context, keywords=keywords)
    response = generic_chat_chain_json(template=template)

    types: List[Type] = []
    for i, name_descr_dict in enumerate([response['node_types'], response['relation_types']]):
        types.extend([Type(
            unique_id=str(uuid.uuid4()),
            type="node_type" if i == 0 else "rel_type",
            value=name,
            description=descr,
        ) for name, descr in name_descr_dict.items()])

    # databases
    if not databases:
        return types

    if Database.MONGO in databases:
        mdb = MongoDBDatabase()
        [mdb.add_entry(type, metadata={'general': True, 'keywords_based': True}) for type in types]
        databases.remove(Database.MONGO)

    if Database.QDRANT in databases:
        qdb = QdrantDatabase()
        [qdb.embedd_and_upsert_record(
            value=type.value+": "+type.description,
            collection_name="graph_types",
            unique_id=type.id,
            metadata={
                "name": type.value,
                "description": type.description
            }
        ) for type in types]
        databases.remove(Database.QDRANT)

    # logging
    logging.basicConfig(level=logging.INFO)
    for database in databases:
        logging.warning(msg=f"No support for {database} in type_extraction_from_keywords_chain")

    return types


