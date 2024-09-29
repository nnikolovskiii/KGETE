from app.chains.generic.models import Database
from app.chains.nodes.transform_rel_chain import transform_rel_chain
from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.models.models import Type

mdb = MongoDBDatabase()
triplets = mdb.get_entries(class_type=Triplet, collection_name='NewTriplet')

relations = set([triplet.relation for triplet in triplets])
mongo_relations = mdb.get_entries(class_type=Type, collection_name='NewType',
                                  doc_filter={"general": True, "type": "rel_type"})
mongo_relations = [relation.value for relation in mongo_relations]

count = 0
curr_relations = []
for relation in relations:
    if count < 10:
        if relation not in mongo_relations:
            count += 1
            curr_relations.append(relation)
    else:
        try:
            transform_rel_chain(
                relations=curr_relations,
                abstract_relations=mongo_relations,
                databases=[Database.MONGO]
            )
        except Exception as e:
            print(f"Problem in mapping types, exception: {e}")
        curr_relations = []
        count = 0
