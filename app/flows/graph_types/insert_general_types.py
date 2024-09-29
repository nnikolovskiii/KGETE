import uuid

from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.models.models import Type


general_types = [
    {
        "type": "node",
        "name": "Entity",
        "description": "Represents anything that exists as a distinct unit, be it physical, conceptual, or abstract.",
        "examples": "Objects, Beings, Ideas"
    },
    {
        "type": "node",
        "name": "Agent",
        "description": "Any node capable of action or influence in a system or context.",
        "examples": "People, Organizations, Systems"
    },
    {
        "type": "node",
        "name": "Object",
        "description": "A passive entity that can be acted upon or used in various contexts.",
        "examples": "Tools, Products, Documents, Artifacts"
    },
    {
        "type": "node",
        "name": "Action",
        "description": "Represents an activity, process, or event that takes place.",
        "examples": "Processes, Transactions, Movements, Transformations"
    },
    {
        "type": "node",
        "name": "State",
        "description": "Describes the condition or situation of an entity at a given point in time.",
        "examples": "Status, Mode, Phase, Context"
    },
    {
        "type": "node",
        "name": "Attribute",
        "description": "Represents properties or characteristics of another node or entity.",
        "examples": "Qualities, Features, Measurements, Descriptions"
    },
    {
        "type": "node",
        "name": "Context",
        "description": "Captures the surrounding circumstances, environment, or conditions related to an entity or event.",
        "examples": "Time, Place, Situation, Conditions"
    },
    {
        "type": "node",
        "name": "Interaction",
        "description": "Represents the relationship or exchange between two or more agents or entities.",
        "examples": "Communication, Collaboration, Conflict, Trade"
    },
    {
        "type": "node",
        "name": "Concept",
        "description": "An abstract idea, category, or theme that represents a general notion or principle.",
        "examples": "Principles, Ideals, Themes, Fields of Study"
    },
    {
        "type": "node",
        "name": "Resource",
        "description": "An asset or item that can be used, consumed, or transformed in some process.",
        "examples": "Materials, Data, Energy, Capital"
    },
    {
        "type": "rel",
        "name": "Related",
        "description": "Connects two entities that are related in some way."
    },
    {
        "type": "rel",
        "name": "Similar",
        "description": "Indicates that two entities share common characteristics."
    },
    {
        "type": "rel",
        "name": "Opposite",
        "description": "Represents a relationship between two entities that are opposite or contrasting."
    },
    {
        "type": "rel",
        "name": "Cause",
        "description": "Establishes a cause-and-effect relationship between two entities."
    },
    {
        "type": "rel",
        "name": "Influence",
        "description": "Suggests that one entity has an impact on another entity."
    },
    {
        "type": "rel",
        "name": "IsA",
        "description": "Represents a relationship where one entity is a subtype or instance of another."
    },
    {
        "type": "rel",
        "name": "PartOf",
        "description": "Indicates that one entity is a component or part of another."
    },
    {
        "type": "rel",
        "name": "Has",
        "description": "Establishes a relationship where one entity has or contains another."
    },
    {
        "type": "rel",
        "name": "Enables",
        "description": "Represents a relationship where one entity enables or facilitates another."
    },
    {
        "type": "rel",
        "name": "Depends",
        "description": "Indicates that one entity relies on or depends on another."
    },
    {
        "type": "rel",
        "name": "RelatedTo",
        "description": "Represents a generic relationship between two entities that are related in some way."
    },
    {
        "type": "rel",
        "name": "Refers",
        "description": "Establishes a relationship between an entity and another entity that it refers to."
    }
]


def insert_general_types():
    mdb = MongoDBDatabase()
    for type in general_types:
        unique_id = str(uuid.uuid4())
        mdb.add_entry(entity=Type(
            id=unique_id,
            type="node_type" if type["type"] == "node" else "rel_type",
            value=type["name"],
            description=type["description"],
        ), collection_name="NewType",
            metadata={
            "general": True
        })
