from app.chains.generic.models import Database
from app.chains.nodes.combine_nodes_chain import combine_nodes_chain, CombineNodesOutput
from app.chains.triplets.extract_triplets_chain import Triplet, Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase

from tqdm import tqdm


mdb = MongoDBDatabase()
node_ids = mdb.get_ids(class_type=Node, doc_filter={"latest": True})

qdb = QdrantDatabase()

for id in tqdm(node_ids, desc="Combining nodes"):
    node = mdb.get_entity(id=id, class_type=Node)
    if not node.latest:
        continue

    point = qdb.retrieve_point(collection_name="nodes", point_id=id)

    similar_points = qdb.search_embeddings(
        query_vector=point.vector,
        collection_name="nodes",
        score_threshold=0.2,
        filter={"latest":True},
        top_k=11,
    )
    similar_points_ids = [point.id for point in similar_points]
    similar_nodes = [mdb.get_entity(id=id, class_type=Node) for id in similar_points_ids]

    output: CombineNodesOutput = combine_nodes_chain(
        node=similar_nodes[0],
        nodes=similar_nodes[1:],
        databases=[Database.MONGO, Database.QDRANT]
    )




