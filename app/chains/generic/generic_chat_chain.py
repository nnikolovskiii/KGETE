from typing import Any, Dict

from app.llms.generic_chat import generic_chat
from app.utils.json_extraction import trim_and_load_json


def generic_chat_chain_json(
        template: str,
        list_name: str = ""
) -> Dict[str, Any]:
    is_finished = False
    json_data = {}
    tries = 0

    while not is_finished:
        if tries > 3:
            raise Exception()

        response = generic_chat(message=template)
        is_finished, json_data = trim_and_load_json(input_string=response, list_name=list_name)
        tries += 1

    return json_data
