from typing import List


def combine_triplets_template(
        contexts: List[str],
        triplets: List[str],
) -> str:
    return f""""Given the provided context and nodes and relationships, try to combine and reduce nodes that mean the same thing, but are worded differently.
    
Example:
Nodes "Poland" and "Country of Poland" -> "Poland"

START CONTEXT

{"\n".join(contexts)}

END CONTEXT

START TRIPLETS

[{"\n".join(triplets)}]

END TRIPLETS
    
Instructions:
    - Never create new relationships and nodes, just reduce and combine the already given. Create only reduced nodes.
    - Base the meaning of the triplets from the context. The triplets were created from the context, so you can use it as a string guideline.


Output Format:

{{
  "groups": [
    {{
      "name": "<reduced node name>",
      "sub_nodes": ["<list of nodes that were reduced>"]
    }},
  ]
}}
"""
