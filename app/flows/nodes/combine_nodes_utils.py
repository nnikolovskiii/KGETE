from typing import Dict, List
from app.chains.triplets.extract_triplets_chain import Node, Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from app.models.models import Type


def check_types():
    mdb = MongoDBDatabase()

    triplets = mdb.get_entries(class_type=Triplet, doc_filter={'version': '4'})
    mongo_node_types = [type.value for type in mdb.get_entries(class_type=Type, doc_filter={'general': True, 'type': 'node_type'})]
    mongo_rel_types = [type.value for type in mdb.get_entries(class_type=Type, doc_filter={'general': True, 'type': 'rel_type'})]

    node_freq = {}
    rel_freq = {}
    node_types = set()
    rel_types = set()
    for triplet in triplets:
        rel_types.add(triplet.relation)
        if triplet.head_type not in node_freq:
            node_freq[triplet.head_type] = 0
        if triplet.tail_type not in node_freq:
            node_freq[triplet.tail_type] = 0
        node_freq[triplet.head_type] += 1
        node_freq[triplet.tail_type] += 1

        if triplet.relation not in rel_freq:
            rel_freq[triplet.relation] = 0
        rel_freq[triplet.relation] += 1

    print(node_freq)
    print(rel_freq)
    print(mongo_node_types)


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


def post_combine_nodes():
    mdb = MongoDBDatabase()

    triplets = mdb.get_entries(class_type=Triplet, doc_filter={'version': '4'})
    for triplet in triplets:
        pass


check_types()