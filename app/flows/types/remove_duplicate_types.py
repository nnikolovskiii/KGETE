from typing import Dict
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Type
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from tqdm import tqdm

mdb = MongoDBDatabase()
qdb = QdrantDatabase()
types = mdb.get_entries(class_type=Type)
unique_types: Dict[str, Type] = {}

for graph_type in types:
    if graph_type.value not in unique_types:
        unique_types[graph_type.value] = graph_type

for graph_type in tqdm(list(unique_types.values())[534:], desc="Extracting unique types:"):
    mdb.add_entry(graph_type, collection_name="UniqueTypes", metadata={"unique_type": "yes"})
    qdb.embedd_and_upsert_record(
        value=f"{graph_type.value}: {graph_type.description}",
        value_type=graph_type.type,
        collection_name="kg_llm_fusion",
        unique_id=graph_type.id,
        metadata={
            "type": graph_type.value,
            "description": graph_type.description,
            "unique_type": "yes"
        }
    )