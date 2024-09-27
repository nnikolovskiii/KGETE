from typing import Dict, List
from app.chains.triplets.extract_triplets_chain import Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase


def pre_combine_nodes():
    mdb = MongoDBDatabase()
    qdb = QdrantDatabase()

    nodes = mdb.get_entries(class_type=Node)
    [mdb.update_entity(entity=node, update={"latest": False, "parent_node": None}) for node in nodes]
    [qdb.update_point(id=node.id, collection_name="nodes", update={"latest": False}) for node in nodes]

    name_nodes_dict: Dict[str, List[Node]] = {}
    for node in nodes:
        if node.value not in name_nodes_dict:
            name_nodes_dict[node.value] = []
        name_nodes_dict[node.value].append(node)

    for name, nodes in name_nodes_dict.items():
        parent_node = nodes[0]
        mdb.update_entity(entity=parent_node, update={"latest": True})
        qdb.update_point(id=parent_node.id, collection_name="nodes", update={"latest": True})

        for node in nodes[1:]:
            mdb.update_entity(entity=node, update={"parent_node": parent_node.id})
