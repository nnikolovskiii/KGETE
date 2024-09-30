from typing import List, Optional

from markdown_it.rules_inline import entity
from pydantic import BaseModel

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.chains.generic.models import Database
from app.chains.triplets.extract_triplets_chain import Node
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from app.databases.qdrant_database.qdrant_database import QdrantDatabase
from app.templates.nodes.combine_nodes_template import combine_nodes_template


class CombineNodesOutput(BaseModel):
    reasoning: str
    verdict: str
    node_indexes: List[int]


def combine_nodes_chain(
        node:Node,
        nodes: List[Node],
        databases: Optional[List[Database]] = None
) -> CombineNodesOutput:
    template = combine_nodes_template(
        node=str(node),
        nodes=["index:" +str(i)+" "+str(node) for i, node in enumerate(nodes)],
    )

    json_data = generic_chat_chain_json(template=template)

    # if "response" not in json_data:
    #     raise Exception("Badly generated response from llm. No key response.")
    # output = CombineNodesOutput(**json_data['response'])
    #
    # # databases
    # if not databases:
    #     return output
    #
    # if Database.MONGO in databases:
    #     mdb = MongoDBDatabase()
    #     if output.verdict == "yes":
    #         for ind in output.node_indexes:
    #             child_node = nodes[ind]
    #             mdb.update_entity(entity=child_node, update={"latest": False, "parent_node": node.id})
    #
    # if Database.QDRANT in databases:
    #     qdb = QdrantDatabase()
    #     if output.verdict == "yes":
    #         for ind in output.node_indexes:
    #             child_node = nodes[ind]
    #             qdb.update_point(collection_name="nodes_rels", id= child_node.id, update={"latest": False})
    #
    # return output

