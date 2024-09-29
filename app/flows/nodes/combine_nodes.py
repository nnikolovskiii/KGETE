import uuid

from app.chains.generic.models import Database
from app.chains.nodes.combine_nodes_chain import combine_nodes_chain, CombineNodesOutput
from app.chains.triplets.extract_triplets_chain import Triplet, Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase

from tqdm import tqdm
from typing import Set, Tuple, Dict


def combine_nodes():
    mdb = MongoDBDatabase()
    node_ids = mdb.get_ids(class_type=Node, doc_filter={"latest": True, "extra": True})

    qdb = QdrantDatabase()

    for id in tqdm(node_ids, desc="Combining nodes"):
        node = mdb.get_entity(id=id, class_type=Node)
        if not node.latest:
            continue
        try:
            point = qdb.retrieve_point(collection_name="nodes", point_id=id)
        except Exception as e:
            print("Id not recognized")
            continue

        similar_points = qdb.search_embeddings(
            query_vector=point.vector,
            collection_name="nodes",
            score_threshold=0.2,
            filter={"latest": True},
            top_k=11,
        )
        similar_points_ids = [point.id for point in similar_points]
        similar_nodes = [mdb.get_entity(id=id, class_type=Node) for id in similar_points_ids]

        output: CombineNodesOutput = combine_nodes_chain(
            node=similar_nodes[0],
            nodes=similar_nodes[1:],
            databases=[Database.MONGO, Database.QDRANT]
        )


def update_triplets(
        backup: bool = False
) -> bool:
    mdb = MongoDBDatabase()
    parent_nodes = mdb.get_entries(class_type=Node, doc_filter={"latest": True})
    child_nodes = mdb.get_entries(class_type=Node, doc_filter={"latest": False})
    print(len(parent_nodes), len(child_nodes))
    parent_count = 0
    child_count = 0
    for node in parent_nodes:
        if node.parent_node is None:
            parent_count+=1

    for node in child_nodes:
        if node.parent_node is None:
            child_count+=1

    print(parent_count, len(parent_nodes))
    print(child_count)

    if backup:
        triplets = mdb.get_entries(class_type=Triplet, doc_filter={"version": "4"})
        for triplet in tqdm(triplets, desc="Backing up triplets"):
            mdb.add_entry(entity=triplet, collection_name="TripletBackup")

    triplets = mdb.get_entries(class_type=Triplet, collection_name="TripletBackup")

    node_parent_dict: Dict[str, Node] = {}
    all_nodes = child_nodes + parent_nodes

    for node in tqdm(all_nodes, desc="Forming dict"):
        parent_node = get_parent(mdb=mdb, node=node)
        if parent_node.parent_node is not None:
            raise Exception("Parent node must not have a parent.")
        node_parent_dict[node.value] = parent_node

    for triplet in tqdm(triplets, desc="Updating triplets:"):
        new_head = node_parent_dict[triplet.head_value]
        new_tail = node_parent_dict[triplet.tail_value]
        triplet.head_value = new_head.value
        triplet.head_type = new_head.type
        triplet.head_description = new_head.description
        triplet.tail_value = new_tail.value
        triplet.tail_type = new_tail.type
        triplet.tail_description = new_tail.description
        mdb.add_entry(entity=triplet, collection_name="TripletActive")

    return verify_update()


def verify_update() -> bool:
    mdb = MongoDBDatabase()
    triplets = mdb.get_entries(class_type=Triplet, collection_name="TripletActive")
    parent_nodes = mdb.get_entries(class_type=Node, doc_filter={"latest": True})
    nodes = set([parent_node.value for parent_node in parent_nodes])
    triplet_nodes: Set[Tuple[str, str, str]] = set()
    for triplet in triplets:
        triplet_nodes.add(triplet.head_value)
        triplet_nodes.add(triplet.tail_value)

    check = [1 for triplet_node in triplet_nodes if triplet_node not in nodes]
    print(len(check))
    return len(check) == 0


def get_parent(
        mdb: MongoDBDatabase,
        node: Node
) -> Node:
    while node.parent_node is not None:
        node = mdb.get_entity(id=node.parent_node, class_type=Node)
    return node
