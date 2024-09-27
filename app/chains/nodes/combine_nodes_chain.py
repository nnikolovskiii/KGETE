import  uuid
from typing import List, Optional

from aiohttp.client_reqrep import json_re

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.chains.generic.models import Database
from app.databases.mongo_database.mongo_database import MongoDBDatabase
from pydantic import BaseModel

from app.templates.nodes.combine_nodes_template import combine_nodes_template


def combine_nodes_chain(
        node:str,
        nodes: List[str],
        databases: Optional[List[Database]] = None
):
    template = combine_nodes_template(
        node=node,
        nodes=nodes,
    )

    json_data = generic_chat_chain_json(template=template)

    if "response" not in json_data:
        raise Exception("Badly generated response from llm. No key response.")
    print(json_data['response'])

    # # databases
    # if not databases:
    #     return reduced_nodes
    #
    # if Database.MONGO in databases:
    #     mdb = MongoDBDatabase()
    #
    #     for reduced_node in reduced_nodes:
    #         mdb.add_entry(entity=reduced_node)
    # return reduced_nodes
