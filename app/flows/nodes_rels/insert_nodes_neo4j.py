from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase

from tqdm import tqdm

from app.databases.neo4j_database.neo4j_database import Neo4jDatabase, NeoRelationship, NeoNode
from app.models.models import Chunk

mdb = MongoDBDatabase()
ndb = Neo4jDatabase()
triplets = mdb.get_entries(class_type=Triplet, collection_name="RelUpdatedTriplet")
print(len(triplets))
chunks = mdb.get_entries(class_type=Chunk)
nodes = {}
unique_triplets = set()

for triplet in triplets:
    unique_triplets.add((triplet.head_value, triplet.relation, triplet.tail_value))

for head_value, relation, tail_value in tqdm(unique_triplets, "Adding triplets to neo4j database"):
    ndb.create_relationship(
        node1=NeoNode(
            value=head_value,
        ),
        node2=NeoNode(
            value=tail_value,
        ),
        relationship=NeoRelationship(
            type=relation
        )
    )
