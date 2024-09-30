from typing import List


def combine_nodes_template(
        node: str,
        nodes: List[str],
) -> str:
    return f""""You are a model that knows how to analyze graphs. You are given a node and your job is to see if there are any other nodes in the provided nodes that are completely similar in meaning.
Analyze each node and for each create a reasoning whether it is identical or not to the given node. If it is completely similar return a verdict "yes", otherwise return a verdict "no".


Given node:
{node}

Other Nodes:
[{"\n\n".join(nodes)}]


Instructions:
    - If some node is completely similar return a verdict "yes". 
    - If some node is not completely identical return a verdict "no".
    - Do not limit yourself to the name and description. Use your knowledge as well.
    - Return in json

Output Format:

{{
    "response":[{{
            "node_index": <node index>,
            "reasoning": <reason if it is completely similar to the given node>,
            "verdict": <is it completely similar to the given node>,
        }}
        ,FOR EACH NODE
    ]
}}
"""
