import uuid

from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.postgres_database.postgres import Type

mdb = MongoDBDatabase()

general_types = [
    {
        "type": "node",
        "name": "Concept",
        "description": "Abstract ideas or notions (e.g., happiness, freedom, justice)"
    },
    {
        "type": "node",
        "name": "Object",
        "description": "Tangible things (e.g., book, car, tree)"
    },
    {
        "type": "node",
        "name": "Person",
        "description": "Individuals (e.g., John, Mary, Albert Einstein)"
    },
    {
        "type": "node",
        "name": "Organization",
        "description": "Groups or institutions (e.g., company, university, government)"
    },
    {
        "type": "node",
        "name": "Location",
        "description": "Places (e.g., city, country, park)"
    },
    {
        "type": "node",
        "name": "Event",
        "description": "Occurrences or happenings (e.g., conference, wedding, earthquake)"
    },
    {
        "type": "node",
        "name": "Product",
        "description": "Goods or services (e.g., phone, software, course)"
    },
    {
        "type": "node",
        "name": "Document",
        "description": "Written or digital content (e.g., article, book, report)"
    },
    {
        "type": "rel",
        "name": "IsA",
        "description": "Hierarchical relationships (e.g., 'car is a vehicle')"
    },
    {
        "type": "rel",
        "name": "PartOf",
        "description": "Composition relationships (e.g., 'engine is part of car')"
    },
    {
        "type": "rel",
        "name": "HasA",
        "description": "Attribute relationships (e.g., 'person has name')"
    },
    {
        "type": "rel",
        "name": "LocatedIn",
        "description": "Spatial relationships (e.g., 'city is located in country')"
    },
    {
        "type": "rel",
        "name": "CreatedBy",
        "description": "Authorship relationships (e.g., 'book was written by author')"
    },
    {
        "type": "rel",
        "name": "RelatedTo",
        "description": "Associative relationships (e.g., 'friend is related to person')"
    },
    {
        "type": "rel",
        "name": "OccursIn",
        "description": "Temporal relationships (e.g., 'event occurs on date')"
    },
    {
        "type": "rel",
        "name": "Cites",
        "description": "Reference relationships (e.g., 'article cites paper')"
    },
    {
        "type": "rel",
        "name": "HasProperty",
        "description": "Attribute-value relationships (e.g., 'person has age 30')"
    },
    {
        "type": "rel",
        "name": "InfluencedBy",
        "description": "Causal relationships (e.g., 'event was influenced by person')"
    }
]


def insert_general_types():
    for type in general_types:
        unique_id = str(uuid.uuid4())
        mdb.add_entry(entity=Type(
            id=unique_id,
            type="node_type" if type["type"] == "node" else "rel_type",
            value=type["name"],
            description=type["description"],
        ), metadata={
            "version": "2",
            "general": True
        })
