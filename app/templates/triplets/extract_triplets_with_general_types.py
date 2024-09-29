from typing import List


def extract_triplets_from_general_template(
        text: str,
        # node_types:List[str],
        rel_types: List[str]
) -> str:
    return f"""You are a graph expert designed to extract triplets from text.
    While creating the triplets NEVER make the node values and the relation a description. Make then a single thing. Make them SHORT.
    
    Example

    {{
      "triplets": [
          {{
            "head_value": "Pots of Honey",
            "relation": "Discovered In",
            "tail_value": "Ancient Egyptian Tombs"
          }},
        ],
    }}

    Text:
    {text}
    
    While creating the triplets think of these things:
        - NEVER use more than three words for node and rel values unless it they are a named entity.
        - Create as many triplets as you can think about. Do not limit yourself to numbers.
        - Keep in mind the direction of the relation.
        - NEVER add measures, numbers, dates and years to the node and tail values.
        - Return in json with keys 'triplets' 
        
    {{
        "triplets": [
            {{
            "head_value": ...
            "relation": ...
            "tail_value": ...
            }}
        ],
      }},
      
    You MUST use these for relations. Cannot use others:
    [{", ".join(rel_types)}]

    """
