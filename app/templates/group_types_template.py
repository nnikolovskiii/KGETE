from typing import List


def group_types_template(
        types: List[str],
        graph_type: str
) -> str:
    return f""""You are a top-tier algorithm designed for extracting information in structured formats to build a knowledge graph. Group the {"node" if graph_type == "node_types" else "relation"} types that are identical and have the same meaning. Do these steps:
1. Think and analyze how you can group the {"node" if graph_type == "node_types" else "relation"} types so that the types in a single group have identical meaning.
2. Group the {"node" if graph_type == "node_types" else "relation"} types and output a json. Also provide a new description for the new groups.

Example:
{{"groups": [
    {{
      "description": "A person or individual engaged in a field or activity",
      "name": "Entity",
      "sub_types": ["Person", "Practitioner"]
    }},
 {{
      "description": "Indicates the containment or location of something within a physical or conceptual space",
      "name": "Location",
      "sub_types": ["Location""]
    }}
]
}}

{"Node types:" if graph_type == "node_types" else "Relation types"}
{"\n".join(types)}

Important:
If types are dissimilar do not group them. 
Return in json format:
"""
