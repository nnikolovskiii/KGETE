from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from tqdm import tqdm

mdb = MongoDBDatabase()
chunks = mdb.get_entries(class_type=Chunk)

qdb = QdrantDatabase()

for chunk in tqdm(chunks, "Adding to qdrant"):
    qdb.embedd_and_upsert_record(
        value=chunk.context,
        collection_name="chunks",
        unique_id=chunk.id,
        metadata={"doc_id": chunk.doc_id},
    )
