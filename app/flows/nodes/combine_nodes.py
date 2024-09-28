import uuid

from app.chains.generic.models import Database
from app.chains.nodes.combine_nodes_chain import combine_nodes_chain, CombineNodesOutput
from app.chains.triplets.extract_triplets_chain import Triplet, Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase

from tqdm import tqdm
from typing import Set, Tuple


def combine_nodes():
    mdb = MongoDBDatabase()
    node_ids = mdb.get_ids(class_type=Node, doc_filter={"latest": True, "extra": True})

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

    for child_node in tqdm(child_nodes, desc="Going through child nodes"):
        triplet = mdb.get_entity(id=child_node.triplet_id, class_type=Triplet, collection_name="TripletBackup")
        if child_node.value == triplet.head_value:
            parent_node = get_parent(mdb=mdb, node=child_node)
            triplet.head_value = parent_node.value
            triplet.head_type = parent_node.type
            triplet.head_description = parent_node.description
            mdb.add_entry(entity=triplet, collection_name="TripletActive")
        elif child_node.value == triplet.tail_value:
            parent_node = get_parent(mdb=mdb, node=child_node)
            triplet.tail_value = parent_node.value
            triplet.tail_type = parent_node.type
            triplet.tail_description = parent_node.description
            mdb.add_entry(entity=triplet, collection_name="TripletActive")
        else:
            print("Problem")

    return verify_update()


def verify_update() -> bool:
    mdb = MongoDBDatabase()
    triplets = mdb.get_entries(class_type=Triplet, collection_name="TripletActive")
    parent_nodes = mdb.get_entries(class_type=Node, doc_filter={"latest": True})
    nodes = set([(parent_node.value, parent_node.type, parent_node.description) for parent_node in parent_nodes])
    triplet_nodes: Set[Tuple[str, str, str]] = set()
    for triplet in triplets:
        triplet_nodes.add((triplet.head_value, triplet.head_type, triplet.head_description))
        triplet_nodes.add((triplet.tail_value, triplet.tail_type, triplet.tail_description))

    check = [triplet_node for triplet_node in triplet_nodes if triplet_node not in nodes]
    print(check)
    return len(check) == 0


def check():
    mdb = MongoDBDatabase()
    qdb = QdrantDatabase()
    triplets = mdb.get_entries(class_type=Triplet, collection_name="TripletBackup")
    qdrant_nodes = set([point.payload["value"].split(":")[0] for point in qdb.get_all_points(collection_name="nodes")])
    nodes = mdb.get_entries(class_type=Node)
    nodes_dict = {node.value:node for node in nodes}
    di = {}
    s1 = set()
    new_nodes = []

    for triplet in tqdm(triplets, desc="Checking triplets"):
        if triplet.head_value not in nodes_dict:
            di[triplet.head_value] = Node(
                id=str(uuid.uuid4()),
                value=triplet.head_value,
                type=triplet.head_type,
                description=triplet.head_description,
                triplet_id=triplet.id,
            )

        if triplet.tail_value not in nodes_dict:
            di[triplet.tail_value] = Node(
                id=str(uuid.uuid4()),
                value=triplet.tail_value,
                type=triplet.tail_type,
                description=triplet.tail_description,
                triplet_id=triplet.id,
            )

        if triplet.head_value not in qdrant_nodes:
            s1.add(triplet.head_value)

        if triplet.tail_value not in qdrant_nodes:
            s1.add(triplet.tail_value)

    for name, node in tqdm(di.items(), desc="F up", total=len(di)):
        mdb.add_entry(entity=node, metadata={"extra": True, "latest": True})
        qdb.embedd_and_upsert_record(
            value=f"{node.value}: {node.description}",
            unique_id=node.id,
            collection_name="nodes",
            metadata={"extra": True, "latest": True},
        )

    print(len(di), len(nodes), len(s1))


def get_parent(
        mdb: MongoDBDatabase,
        node: Node
) -> Node:
    while node.parent_node is not None:
        node = mdb.get_entity(id=node.parent_node, class_type=Node)
    return node


check()
combine_nodes()
