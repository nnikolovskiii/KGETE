from tqdm import tqdm

from app.chains.graph_types.group_types_chain import group_types_chain
from app.chains.graph_types.types_extraction_chain import node_rel_type_extraction_chain
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk


mdb = MongoDBDatabase()

chunks = mdb.get_entries(class_type=Chunk)

for chunk in tqdm(chunks[:20]):
    node_rel_type_extraction_chain(
        text=chunk.context,
    )

for i in [0, 1]:
    group_types_chain(level=i)
