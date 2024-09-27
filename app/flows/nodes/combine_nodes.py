from app.chains.nodes.combine_nodes_chain import combine_nodes_chain
from app.chains.triplets.extract_triplets_chain import Triplet, Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase


mdb = MongoDBDatabase()
nodes= mdb.get_entries(class_type=Node)

nodes_di = {}
for node in nodes:
    nodes_di[f"{node.value}{node.type}"] = node

qdb = QdrantDatabase()

node_ids = [node.id for node in nodes_di.values()]
points = [qdb.retrieve_point(collection_name="nodes", point_id=node_id) for node_id in node_ids]

for point in points[:20]:
    similar_points = qdb.search_embeddings(
        query_vector=point.vector,
        collection_name="nodes",
        score_threshold=0.2,
        filter={"unique":True},
        top_k=8,
    )
    similar_points_ids = [point.id for point in similar_points]
    similar_nodes = [mdb.get_entity(id=id, class_type=Node) for id in similar_points_ids]
    print("\n".join([str(node) for node in similar_nodes]))

    nodes = ["index:" +str(i)+" "+str(node) for i, node in enumerate(similar_nodes[1:])]

    reduced_nodes= combine_nodes_chain(
        node=str(similar_nodes[0]),
        nodes=nodes,
    )

    # for reduced_node in reduced_nodes:
    #     print(f"{reduced_node.new_node}: {reduced_node.reduced_nodes}")


