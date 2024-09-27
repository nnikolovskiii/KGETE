def combine_cluster_nodes_template(
        nodes: str,
) -> str:
    return f""""Given the provided nodes and there descriptions, try to combine and reduce nodes that mean the same thing, but are worded differently.
    
Example:
{{
    "reduced_nodes_li":[{{
        "reasoning": "All terms refer to the same landmass located in Central Europe."
        "description": "Poland is a country in Central Europe known for its rich history, medieval architecture, diverse landscapes, and vibrant cultural heritage."
        "new_node": "Poland",
        "reduced_nodes": ["Republic of Poland", "Country of Poland"]
    }}]
}}


Nodes:
[{nodes}]

    
Instructions:
    - Create only reduced nodes. If there is a node that cannot be reduced do not add it to the response.
    - You need multiple nodes wit hth the same meaning to have a reduced node. You cannot reduce a single node.
    - Use the description and node types as the only source of knowledge for reducing the nodes.
    - Return in json

Output Format:

{{
    "reduced_nodes_li":[{{
        "reasoning": ...
        "new_node": ...,
        "description": ...
        "reduced_nodes": [...]
    }}
    ]
}}
"""
