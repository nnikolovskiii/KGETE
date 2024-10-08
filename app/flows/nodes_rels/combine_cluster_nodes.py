from typing import List
from tqdm import tqdm
from app.chains.generic.models import Database
from app.chains.nodes.combine_cluster_nodes_template import ReducedNode, combine_cluster_nodes_chain
from app.chains.triplets.extract_triplets_chain import Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from app.flows.utils.clustering_vectors import cluster_vectors

mdb = MongoDBDatabase()
nodes= mdb.get_entries(class_type=Node)

nodes_di = {}
for node in nodes:
    nodes_di[f"{node.value}{node.type}"] = node

qdb = QdrantDatabase()

node_ids = [node.id for node in nodes_di.values()]

clusters:List[List[str]] = cluster_vectors(
    vector_ids=node_ids,
    qdb=qdb,
)

for cluster in tqdm(clusters[:10], desc="Reducing nodes_rels"):
    cluster_nodes = [mdb.get_entity(id=id, class_type=Node) for id in cluster]
    nodes = "\n".join([str(node) for node in cluster_nodes])

    reduced_nodes: List[ReducedNode] = combine_cluster_nodes_chain(
        nodes=nodes,
        databases=[Database.MONGO]
    )

    for reduced_node in reduced_nodes:
        print(f"{reduced_node.new_node}: {reduced_node.reduced_nodes}")


