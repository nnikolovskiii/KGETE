from typing import List


def extract_triplets_from_general_template(
        text: str,
        node_types:List[str],
        rel_types: List[str]
) -> str:
    return f"""### Instructions
    Your job is to extract triplets from the given text.
       - **(Node: A) - [Relation] → (Node: B)**
       - **(Node: C) - [Relation] → (Node: D)**

    ### Example

    {{
      "triplets": [
          {{
            "head_type": "Artifact",
            "head_value": "Pots of Honey",
            "relation": "Discovered In",
            "tail_type": "Location",
            "tail_value": "Ancient Egyptian Tombs"
          }},
        ],
    }}

    ### Text:
    {text}


    ### Node types:
    [{",".join(node_types)}]
    
    Important: You MUST use the given node types for generating the triplets
    
    ### Relation types:
    [{",".join(rel_types)}]

    Important: You MUST use the given relation types for generating the triplets

    ### Important instructions
        - NEVER use more than three words for node and rel values unless it they are a named entity.
        - NEVER make the node and rel values a description. Make then a single thing. Make them SHORT.
        - Create as many triplets as you can think about. Do not limit yourself to numbers.
        - Keep in mind the direction of the relation. Square IsA Rectangle is correct, but Rectangle IsA Square is not correct.
        - Return in json with keys 'triplets' 
    {{
        "triplets": [
            {{
            "head_type": ...
            "head_value": ...
            "relation": ...
            "tail_type": ...
            "tail_value": ...
            }}
        ],
      }},
    """
