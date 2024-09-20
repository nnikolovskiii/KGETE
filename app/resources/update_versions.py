from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Type
from app.modeling.hgt_train import metadata

mdb = MongoDBDatabase()

types = mdb.get_entries(class_type=Type)
[mdb.update_entity(entity=type, update={"version": "1"}) for type in types]

print("Finished updating versions")
