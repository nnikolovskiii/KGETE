import uuid
from typing import List, Tuple
from tqdm import tqdm

from app.chains.graph_types.group_types_chain import group_types_chain, GroupType
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Type
from app.databases.qdrant_database.qdrant_database import QdrantDatabase

from app.flows.utils.clustering_vectors import cluster_vectors


mdb = MongoDBDatabase()
qdb = QdrantDatabase()

graph_type = "node_type"

type_ids = mdb.get_ids(class_type=Type, collection_name="UniqueTypes",  doc_filter={"type": graph_type})

clusters:List[List[str]] = cluster_vectors(
    vector_ids=type_ids,
    qdb=qdb,
)

clusters_types = [[mdb.get_entity(type_id, class_type=Type, collection_name="UniqueTypes") for type_id in cluster] for cluster in clusters]

for cluster_num, cluster in tqdm(enumerate(clusters_types), desc="Processing Clusters", total=len(clusters_types)):
    type_dict = {type.value: type for type in cluster}
    group_type_strings = group_types_chain(types=[str(type.value) for type in cluster])
    group_types: List[GroupType] = []

    for group_str in tqdm(group_type_strings, desc=f"Processing Groups in cluster {cluster_num}"):
        parent_id = str(uuid.uuid4())
        parent_type = Type(id=parent_id, type=graph_type, value=group_str.name, description=group_str.description)
        mdb.add_entry(parent_type, collection_name="UniqueTypes" ,metadata={"group": 1})
        qdb.embedd_and_upsert_record(
            value=str(parent_type),
            collection_name="kg_llm_fusion",
            unique_id=parent_id,
            metadata={
                "value": parent_type.value,
                "description": parent_type.description,
                "group": 1
            }
        )

        # noinspection PyTypeChecker
        sub_types: List[Type] = [type_dict[type_name] for type_name in group_str.sub_types if type_name in type_dict]

        group_id = str(uuid.uuid4())
        group_type = GroupType(id=group_id, parent_type=parent_type, sub_types=sub_types)
        mdb.add_entry(group_type, metadata={"group": 1})

        group_types.append(group_type)

