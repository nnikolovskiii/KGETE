import uuid
from typing import Dict

from app.chains.nodes.create_description_chain import create_description_chain
from app.chains.triplets.extract_triplets_chain import Triplet, Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.models.models import Chunk
from tqdm import tqdm

mdb = MongoDBDatabase()

chunks = mdb.get_entries(class_type=Chunk)

for chunk in tqdm(chunks, desc="Create node descriptions"):
    try:
        triplets = mdb.get_entries(
            class_type=Triplet,
            collection_name="RelUpdatedTriplet",
            doc_filter={"chunk_id": chunk.id}
        )

        nodes = set()
        check = [triplet.id for triplet in triplets if triplet.head_id == None or triplet.tail_id == None]

        if len(triplets) > 0 and len(check) != 0:
            for triplet in triplets:
                nodes.add(triplet.head_value)
                nodes.add(triplet.tail_value)

            name_descr_dict = create_description_chain(
                terms=nodes,
                context=chunk.context
            )
            new_nodes:Dict[str, Node] = {}
            for name, descr in name_descr_dict.items():
                new_node = Node(
                    id=str(uuid.uuid4()),
                    name=name,
                    description=descr,
                )

                new_nodes[name] = new_node

                mdb.add_entry(entity=new_node, collection_name="NewNode")

            for triplet in triplets:
                head_node = new_nodes[triplet.head_value]
                tail_node = new_nodes[triplet.tail_value]
                triplet.head_id = head_node.id
                triplet.tail_id = tail_node.id
                mdb.update_entity(entity=triplet, collection_name="RelUpdatedTriplet")

    except Exception as e:
        print("Problem creating node descriptions")
        continue

