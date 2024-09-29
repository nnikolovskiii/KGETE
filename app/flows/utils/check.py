from app.chains.triplets.extract_triplets_chain import Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase


def check_nodes():
    qdb = QdrantDatabase()
    qdb.delete_points(collection_name="nodes_rels", filter={"node_type": "tail"})
