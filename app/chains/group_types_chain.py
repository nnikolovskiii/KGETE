from typing import List
from app.databases.postgres_database.postgres import Type
from app.llms.nim.chat import chat_with_llama70
from app.llms.openai.chat import chat_with_openai
from app.templates.group_types_template import group_types_template
from pydantic import BaseModel
from app.utils.json_extraction import trim_and_load_json


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

    is_finished = False
    json_data = {}
    while not is_finished:
        response = chat_with_llama70(message=template)
        is_finished, json_data = trim_and_load_json(input_string=response, list_name="groups")

    return [GroupTypeString(**json_entry) for json_entry in json_data["groups"]]