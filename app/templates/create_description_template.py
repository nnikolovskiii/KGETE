from typing import List


def create_description_template(
        terms: List[str],
        context: str
):
  return f"""You have the main goal to provide descriptions for the given terms based on the provided context.

    ### Example

    {{
     "descriptions": {{
        "Pots of Honey": "Pots of Honey are ancient or historical containers used to store honey...",
        "Ancient Egyptian Tombs": "Ancient Egyptian Tombs are burial sites used to house the remains of the deceased..."
      }},
    }}

    ### Context:
    {context}


    ### Terms:
    [{",".join(terms)}]

    ### Important instructions
        - You must provide description for each given term
        - Create the description based on the context
        - Return in JSON
    {{
        "descriptions": {{
            "<name of term>": "<description of term>"
        }},
      }},
    """