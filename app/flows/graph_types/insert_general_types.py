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
        "name": "Has",
        "description": "Expresses possession, ownership, or inclusion of one entity by another.",
        "examples": "Entity has Attribute, Agent has Resource"
    },
    {
        "type": "rel",
        "name": "Relates to",
        "description": "A broad, non-specific connection between two entities, without implying hierarchy or causality.",
        "examples": "Entity relates to Entity"
    },
    {
        "type": "rel",
        "name": "Influences",
        "description": "Describes a cause-effect or impact relationship between entities or agents.",
        "examples": "Agent influences Action, Action influences State"
    },
    {
        "type": "rel",
        "name": "Transforms",
        "description": "Captures the change from one form, state, or condition to another.",
        "examples": "Action transforms Object, Context transforms State"
    },
    {
        "type": "rel",
        "name": "Belongs to",
        "description": "Indicates ownership, membership, or association of one entity with another.",
        "examples": "Entity belongs to Context, Agent belongs to Entity"
    },
    {
        "type": "rel",
        "name": "Exists in",
        "description": "Describes the physical or conceptual location of an entity or event within a context.",
        "examples": "Entity exists in Context"
    },
    {
        "type": "rel",
        "name": "Interacts with",
        "description": "Captures the action, communication, or exchange between two or more entities or agents.",
        "examples": "Agent interacts with Agent, Object interacts with Action"
    },
    {
        "type": "rel",
        "name": "Represents",
        "description": "Maps one entity to another as a symbol, model, or representation.",
        "examples": "Concept represents Entity, Agent represents Object"
    },
    {
        "type": "rel",
        "name": "Depends on",
        "description": "Expresses reliance or dependency of one entity or event on another.",
        "examples": "Action depends on Resource, State depends on Context"
    },
    {
        "type": "rel",
        "name": "Creates",
        "description": "Indicates the generation, initiation, or bringing into existence of something by an agent or event.",
        "examples": "Agent creates Action, Context creates Event"
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
            examples = type["examples"]
        ), collection_name="NewType",
            metadata={
            "general": True
        })
