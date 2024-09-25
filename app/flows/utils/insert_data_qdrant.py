import logging
import uuid

from app.chains.triplets.extract_triplets_chain import Triplet, Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from tqdm import tqdm



def insert_chunks():
    mdb = MongoDBDatabase()
    chunks = mdb.get_entries(class_type=Chunk)

    qdb = QdrantDatabase()

    for chunk in tqdm(chunks, "Adding chunks to qdrant"):
        qdb.embedd_and_upsert_record(
            value=chunk.context,
            collection_name="chunks",
            unique_id=chunk.id,
            metadata={"doc_id": chunk.doc_id},
        )

def insert_triplets():
    mdb = MongoDBDatabase()
    qdb = QdrantDatabase()

    while True:
        node_records = qdb.get_all_points(collection_name="nodes", filter={"node_type": "tail"})
        embedded_node_ids = [record.id for record in node_records]
        nodes = mdb.get_entries(class_type=Node, doc_filter={"node_type": "tail"})
        not_embedded_nodes = [node for node in nodes if node.id not in embedded_node_ids]
        print(f"Not embedded nodes number: {len(not_embedded_nodes)}")
        if len(not_embedded_nodes) == 0:
            break


        for node in tqdm(not_embedded_nodes, "Adding nodes to qdrant"):
            try:
                # qdb.embedd_and_upsert_record(
                #     value=f"Name:{triplet.head_value}\nType:{triplet.head_type}\nDescription:{triplet.head_description}",
                #     collection_name="nodes",
                #     unique_id=triplet.id,
                #     metadata={"version": "4"}
                # )
                qdb.embedd_and_upsert_record(
                    value=f"{node.value}:{node.description}",
                    collection_name="nodes",
                    unique_id=node.id,
                    metadata={"node_type":"tail"}
                )
            except Exception as e:
                logging.warning("There was a problem with the api")

def mv_triplets_to_nodes():
    mdb = MongoDBDatabase()
    mdb.delete_collection("Node")
    triplets = mdb.get_entries(class_type=Triplet, doc_filter={"version": "4"})
    head_nodes = set()
    tail_nodes = set()
    for triplet in triplets:
        head_node = Node(
            id=str(uuid.uuid4()),
            value=triplet.head_value,
            description=triplet.head_description,
            type=triplet.head_type,
            triplet_id=triplet.id
        )
        tail_node = Node(
            id=str(uuid.uuid4()),
            value=triplet.head_value,
            description=triplet.head_description,
            type=triplet.head_type,
            triplet_id=triplet.id
        )
        head_nodes.add(head_node)
        tail_nodes.add(tail_node)

    for head_node in head_nodes:
        mdb.add_entry(head_node, metadata={"node_type": "head"})
    for tail_node in tail_nodes:
        mdb.add_entry(tail_node, metadata={"node_type": "tail"})

    qdb = QdrantDatabase()
    qdb.delete_collection("nodes")
    triplet_records = qdb.get_all_points(
        collection_name="triplets",
        filter={"version": "4"},
        with_vectors=True
    )

    head_nodes = mdb.get_entries(class_type=Node, doc_filter={"node_type": "head"})
    di = {}
    for head_node in head_nodes:
        if head_node.triplet_id in di:
            print("Problem")
        di[head_node.triplet_id] = head_node.id

    print(len(head_nodes))

    for record in tqdm(triplet_records, desc="Move triplets to nodes"):
        if record.id not in di:
            continue
        payload = record.payload
        payload["triplet_id"] = record.id
        payload["node_type"] = "head"
        qdb.upsert_record(
            unique_id=di[record.id],
            collection_name="nodes",
            payload=payload,
            vector=record.vector
        )

insert_triplets()
