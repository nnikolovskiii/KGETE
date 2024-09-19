from app.chains.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.neo4j_database.neo4j_database import Neo4jDataset, Node, Relationship
from tqdm import tqdm

mdb = MongoDBDatabase()
ndb = Neo4jDataset()
triplets = mdb.get_entries(class_type=Triplet)

for triplet in tqdm(triplets, desc="Extracting triplets from chunks"):
    ndb.create_relationship(
        node1=Node(
            type=triplet.head_type,
            value=triplet.head_value
        ),
        node2=Node(
            type=triplet.tail_type,
            value=triplet.tail_value
        ),
        relationship=Relationship(
            type=triplet.relation,
        )
    )
