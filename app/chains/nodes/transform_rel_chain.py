from typing import List, Optional

from markdown_it.rules_inline import entity
from pydantic import BaseModel

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_chain import Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from app.templates.nodes.combine_nodes_template import combine_nodes_template
from app.templates.nodes.transform_rel_template import transform_rel_template


class TransformRelOutput(BaseModel):
    id: Optional[str] = None
    reasoning: str
    relation: str
    abstract_relation: str


def transform_rel_chain(
        relations:List[str],
        abstract_relations: List[str],
        databases: Optional[List[Database]] = None
) -> List[TransformRelOutput]:
    template = transform_rel_template(
        relations=relations,
        abstract_relations=abstract_relations,
    )

    json_data = generic_chat_chain_json(template=template)

    if "response" not in json_data:
        raise Exception("Badly generated response from llm. No key response.")

    outputs = [TransformRelOutput(**json) for json in json_data['response']]

    for output in outputs:
        if output.abstract_relation not in abstract_relations:
            raise Exception("Badly generated response from llm. Abstract relation type does not match.")
        if output.relation not in relations:
            raise Exception("Badly generated response from llm. Relation type does not match.")

    # databases
    if not databases:
        return outputs

    if Database.MONGO in databases:
        mdb = MongoDBDatabase()
        for output in outputs:
            import uuid
            output.id = str(uuid.uuid4())
            mdb.add_entry(entity=output)

    return outputs

