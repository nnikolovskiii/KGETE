from typing import Dict

from app.chains.generic.models import Database
from app.chains.nodes.transform_rel_chain import transform_rel_chain, TransformRelOutput
from app.chains.triplets.extract_triplets_chain import Triplet
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.models.models import Type
from tqdm import tqdm


def transform_rels()->None:
    mdb = MongoDBDatabase()
    triplets = mdb.get_entries(class_type=Triplet, collection_name='NewTriplet')

    existing_rels = [output.relation for output in mdb.get_entries(class_type=TransformRelOutput)]

    relations = set([triplet.relation for triplet in triplets])
    relations = [relation for relation in relations if relation not in existing_rels]
    mongo_relations = mdb.get_entries(class_type=Type, collection_name='NewType',
                                      doc_filter={"general": True, "type": "rel_type"})
    mongo_relations = [relation.value for relation in mongo_relations]

    print(mongo_relations)

    count = 0
    curr_relations = []
    for i, relation in tqdm(enumerate(relations), desc="Transforming rels"):
        if count < 10 and len(relations)-1 != i:
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

def update_rels():
    mdb = MongoDBDatabase()
    triplets = mdb.get_entries(class_type=Triplet, collection_name='NewTriplet')

    rel_abstract_dict: Dict[str, str] = {output.relation: output.abstract_relation for output in mdb.get_entries(class_type=TransformRelOutput)}
    abstract_relations = mdb.get_entries(class_type=Type, collection_name='NewType',
                                      doc_filter={"general": True, "type": "rel_type"})
    abstract_relations = [relation.value for relation in abstract_relations]
    for relation in abstract_relations:
        rel_abstract_dict[relation] = relation

    for triplet in tqdm(triplets, desc="Updating triplet relations"):
        new_rel = rel_abstract_dict[triplet.relation]
        triplet.relation = new_rel
        mdb.add_entry(entity=triplet, collection_name="RelUpdatedTriplet")


transform_rels()
