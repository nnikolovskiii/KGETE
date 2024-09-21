from typing import List

from app.chains.generic.models import Database
from app.chains.triplets.combine_triplets_chain import extract_triplets_from_general_chain
from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk
from app.databases.qdrant_database.qdrant_database import QdrantDatabase

mdb = MongoDBDatabase()
chunks= mdb.get_entries(class_type=Chunk)

qdb = QdrantDatabase()

for chunk in chunks[:1]:
    point = qdb.retrieve_point(
        collection_name='chunks',
        point_id=chunk.id,
    )

    similar_points = qdb.search_embeddings(
        query_vector=point.vector,
        collection_name='chunks',
        score_threshold=0.2,
        top_k=2,
    )

    print(len(similar_points))

    contexts: List[str] = [point.payload["value"] for point in similar_points]
    chunk_ids: List[str] = [point.id for point in similar_points]

    triplets: List[Triplet] = []
    [triplets.extend(mdb.get_entries(
        class_type=Triplet,
        doc_filter={"chunk_id": chunk_id, "version":"2"}
    )) for chunk_id in chunk_ids]

    extract_triplets_from_general_chain(
        triplets=triplets,
        contexts=contexts,
        databases=[Database.MONGO]
    )
    print(len(triplets))
    print(triplets)


