from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.chains.utils import save_group_and_types, TypesOutput
from app.templates.graph_types.node_rel_type_extraction import node_rel_type_extraction_template


def node_rel_type_extraction_chain(
        text: str,
):
    template = node_rel_type_extraction_template(text=text)

    json_data = generic_chat_chain_json(template)
    types_output = TypesOutput(**json_data)

    save_group_and_types(
        text=text,
        types_output=types_output
    )

