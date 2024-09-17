import json
from typing import Tuple, Any
from langchain_experimental.graph_transformers import LLMGraphTransformer


def trim_and_load_json(input_string: str, list_name: str = "") -> Tuple[bool, Any]:
    start = input_string.find("{")
    end = input_string.rfind("}") + 1

    if end == 0 and start != -1:
        end = len(input_string)
        input_string += "}"

    json_str = input_string[start:end] if start != -1 and end != 0 else ""

    try:
        return True, json.loads(json_str)
    except json.JSONDecodeError:
        try:
            json_str = f'{{"{list_name}":[{json_str}]}}'
            return True, json.loads(json_str)
        except json.JSONDecodeError:
            return False, None
    except Exception:
        return False, None





