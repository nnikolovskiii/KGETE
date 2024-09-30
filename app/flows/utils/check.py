import uuid
from typing import List

from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_chain import Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from tqdm import tqdm


def create_unique_nodes():
    mdb = MongoDBDatabase()
    qdb = QdrantDatabase()
    nodes = mdb.get_entries(class_type=Node, collection_name='NewNode')
    name_nodes_dict = {}

    for node in nodes:
        if node.name not in name_nodes_dict:
            name_nodes_dict[node.name] = []

        name_nodes_dict[node.name].append(node)

    for name, nodes in tqdm(name_nodes_dict.items(), total=len(name_nodes_dict), desc='Creating unique nodes'):
        count = 0
        context = ""
        while True:
            if count >= len(nodes) or count == 3:
                break
            if count == 0:
                context += nodes[count].description
            else:
                context += "\n" + nodes[count].description
            count += 1

        node = Node(
            id=str(uuid.uuid4()),
            name=name,
            description=context,
            latest=True
        )

        mdb.add_entry(entity=node, collection_name='UpdatedNode')


def upsert_nodes():
    mdb = MongoDBDatabase()
    qdb = QdrantDatabase()
    existing_ids = [point.id for point in qdb.get_all_points(collection_name="unique_nodes")]
    nodes = [node for node in mdb.get_entries(class_type=Node, collection_name='UpdatedNode') if node.id not in existing_ids]
    print(len(nodes))
    for node in tqdm(nodes, desc='Upserting nodes to qdrant'):
        try:
            qdb.embedd_and_upsert_record(
                value=f"Term: {node.name}, Description: {node.description}",
                unique_id=node.id,
                collection_name='unique_nodes',
                metadata={"name": node.name, "description": node.description, "latest": True},
            )
        except Exception as e:
            print("Problem occurred")
            continue


upsert_nodes()
