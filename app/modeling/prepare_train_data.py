from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.models.models import Chunk

mdb = MongoDBDatabase()
triplets = mdb.get_entries(class_type=Triplet, collection_name='RelUpdatedTriplet')
chunks = mdb.get_entries(class_type=Chunk)


