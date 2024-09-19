import uuid
from typing import Dict, List

from app.chains.group_types_chain import group_types_chain, GroupType
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Type, Chunk
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
import random

mdb = MongoDBDatabase()
qdb = QdrantDatabase()
types = mdb.get_entries(class_type=Type)
unique_types: Dict[str, Type] = {}

for graph_type in types:
    if graph_type.value not in unique_types:
        unique_types[graph_type.value] = graph_type

# for graph_type in unique_types.values():
#     mdb.add_entry(graph_type, metadata={"unique_type": "yes"})
#     qdb.embedd_and_upsert_record(
#         value=f"{graph_type.value}: {graph_type.description}",
#         value_type=graph_type.type,
#         collection_name="kg_llm_fusion",
#         unique_id=graph_type.id,
#         metadata={
#             "type": graph_type.value,
#             "description": graph_type.description
#         }
#     )

print("lol")

# graph_type = "rel_type"
#
# type_ids = mdb.get_ids(class_type=Type, doc_filter={"type": graph_type, "unique_type": "yes"})
# all_types = mdb.get_entries(class_type=Type, doc_filter={"type": graph_type, "unique_type": "yes"})
# type_dict: Dict[str, Type] = {graph_type.value: graph_type for graph_type in all_types}
#
# random_type_id = random.choice(type_ids)
# random_point = qdb.retrieve_point(
#     collection_name="kg_llm_fusion",
#     point_id=random_type_id
# )
#
# records = qdb.search_embeddings(
#     query_vector=random_point.vector,
#     collection_name="kg_llm_fusion",
#     score_threshold=0.01,
#     top_k=20,
#     filter_type=graph_type
# )
#
# types = [record.payload['value'] for record in records if "value" in record.payload.keys()]
# group_type_strings = group_types_chain(types=types, graph_type=graph_type)
# group_types: List[GroupType] = []
#
# for group_str in group_type_strings:
#     parent_id = str(uuid.uuid4())
#     parent_type = Type(id=parent_id, type=graph_type, value=group_str.name, description=group_str.description)
#     mdb.add_entry(parent_type)
#
#     sub_types: List[Type] = [type_dict[type_name] for type_name in group_str.sub_types]
#     [mdb.update_entity(sub_type, update={"parent_type": parent_id}) for sub_type in sub_types]
#
#     group_id = str(uuid.uuid4())
#     group_type = GroupType(id=group_id, parent_type=parent_type, sub_types=sub_types)
#     group_types.append(group_type)
#
# print("lol")
#
# context = "\n".join(chunks)
#
# qa_output = qa_generation_chain(context=context)
#
# mdb.add_entry(
#     entity=qa_output,
#     metadata={
#         "top_k": 5,
#         "score_threshold": 0.5,
#         "template": qa_generation_template(context=""),
#     }
# )
