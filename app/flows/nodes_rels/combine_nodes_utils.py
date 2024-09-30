from typing import Dict, List, Tuple
from app.chains.triplets.extract_triplets_chain import Node, Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from app.models.models import Type
import numpy as np


def check_types():
    mdb = MongoDBDatabase()

    triplets = mdb.get_entries(class_type=Triplet, collection_name="TripletActive")
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

    print(f"node_freq: {node_freq}")
    print(f"rel_freq: {rel_freq}")
    print(f"general_types: {mongo_node_types}")

    node_types = calculate_z_scores(elem_frequencies=tuple(node_freq.items()))
    print(node_types)


def pre_combine_nodes():
    mdb = MongoDBDatabase()
    qdb = QdrantDatabase()

    nodes = mdb.get_entries(class_type=Node, collection_name="NewNode")
    [mdb.update_entity(entity=node, collection_name="NewNode", update={"latest": False, "parent_node": None}) for node in nodes]

    name_nodes_dict: Dict[str, List[Node]] = {}
    for node in nodes:
        if node.name not in name_nodes_dict:
            name_nodes_dict[node.name] = []
        name_nodes_dict[node.name].append(node)

    for name, nodes in name_nodes_dict.items():
        parent_node = nodes[0]
        mdb.update_entity(entity=parent_node, collection_name="NewNode", update={"latest": True})
        qdb.update_point(id=parent_node.id, collection_name="nodes_rels", update={"latest": True})

        for node in nodes[1:]:
            mdb.update_entity(entity=node, update={"parent_node": parent_node.id})


def post_combine_nodes():
    mdb = MongoDBDatabase()

    triplets = mdb.get_entries(class_type=Triplet, doc_filter={'version': '4'})
    for triplet in triplets:
        pass


def calculate_z_scores(
        elem_frequencies: Tuple[str, int],
        threshold: float = 0.0
):
    frequencies = [freq for elem, freq in elem_frequencies]
    elements = [elem for elem, freq in elem_frequencies]

    mean_freq = np.mean(frequencies)
    std_freq = np.std(frequencies)

    z_scores = [(x - mean_freq) / std_freq for x in frequencies]

    indexes = [ind for ind, z in zip(range(len(z_scores)), z_scores) if z > threshold]

    print("Z-scores:", z_scores)
    print("Filtered frequencies (Z-score > threshold):", indexes)

    return [elem for ind, elem in enumerate(elements) if ind in indexes]


check_types()