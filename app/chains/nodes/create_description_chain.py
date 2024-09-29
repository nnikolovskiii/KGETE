from typing import List, Dict
from app.chains.generic.generic_chat_chain import generic_chat_chain_json
from app.templates.utils.create_description_template import create_description_template


def create_description_chain(
        context: str,
        terms: List[str]
) -> Dict[str, str]:
    template = create_description_template(
        context=context,
        terms=terms
    )

    json_data = generic_chat_chain_json(template=template)

    if "descriptions" in json_data:
        term_descr_pairs = json_data["descriptions"]
        check = [1 for term, descr in term_descr_pairs.items() if term not in terms]
        if len(check) > 1:
            raise Exception("There are missing terms which are not generated.")

        return term_descr_pairs
    else:
        raise Exception("Badly generated response from llm. No key descriptions.")
