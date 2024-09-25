from typing import List

from app.chains.generic.models import Database
from app.chains.triplets.combine_triplets_chain import combine_triplets_chain, ReducedNode
from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase

mdb = MongoDBDatabase()
triplets= mdb.get_entries(class_type=Triplet, doc_filter={"version": "4"})
qdb = QdrantDatabase()

for triplet in triplets:
    point = qdb.retrieve_point(
        collection_name='triplets',
        point_id=triplet.id,
    )

    similar_points = qdb.search_embeddings(
        query_vector=point.vector,
        collection_name='triplets',
        score_threshold=0.2,
        top_k=10,
        filter={"version": "4"}
    )

    context_triplets: List[Triplet] = [mdb.get_entity(id=point.id, class_type=Triplet) for point in similar_points]
    nodes = "\n".join([triplet.str_with_description() for triplet in context_triplets])

    reduced_nodes: List[ReducedNode] = combine_triplets_chain(
        nodes=nodes,
        databases=[Database.MONGO]
    )
    print(len(triplets))
    print(reduced_nodes)


