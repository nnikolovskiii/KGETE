from typing import List

from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.databases.postgres_database.postgres import Type
from app.templates.graph_types.group_types_template import group_types_template
from pydantic import BaseModel


class GroupTypeString(BaseModel):
    description: str
    name: str
    sub_types: List[str]


class GroupType(BaseModel):
    id: str
    parent_type: Type
    sub_types: List[Type]


def group_types_chain(
        types: List[str],
) -> List[GroupTypeString]:
    template = group_types_template(types=[str(single_type) for single_type in types])

    json_data = generic_chat_chain_json(template=template, list_name="groups")

    return [GroupTypeString(**json_entry) for json_entry in json_data["groups"]]