from app.chains.triplets.extract_triplets_chain import extract_triplets_chain
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Chunk
from tqdm import tqdm


mdb = MongoDBDatabase()
chunks = mdb.get_entries(class_type=Chunk)

for chunk in tqdm(chunks[95:], desc="Extracting triplets from chunks"):
    print()
    print(chunk.context)
    extract_triplets_chain(
        chunk=chunk,
    )
