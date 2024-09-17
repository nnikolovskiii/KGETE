from app.chains.utils import save_group_and_types, TypesOutput
from app.llms.openai.chat import chat_with_openai
from app.templates.node_rel_type_extraction import node_rel_type_extraction_template
from app.utils.json_extraction import trim_and_load_json


def node_rel_type_extraction_chain(
        text: str,
):
    template = node_rel_type_extraction_template(text=text)

    is_finished = False
    json_data = ""
    while not is_finished:
        response = chat_with_openai(message=template)
        is_finished, json_data = trim_and_load_json(response)
    types_output = TypesOutput(**json_data)

    save_group_and_types(
        text=text,
        types_output=types_output
    )

