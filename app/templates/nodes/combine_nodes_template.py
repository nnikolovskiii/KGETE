from typing import List


def combine_nodes_template(
        node: str,
        nodes: List[str],
) -> str:
    return f""""You are a model that knows how to analyze graphs. You are given a node and your job is to see if there are any other nodes in the provided nodes that are highly similar in meaning.
Steps you need to take:
1. Reason whether there are any other nodes that can be combined to the given node. If there is none, just return verdict "no.
2. If there are nodes that can be combined to the given node return them ALL in a list and return verdict "yes".


Given node:
{node}

Other Nodes:
[{"\n".join(nodes)}]


Instructions:
    - If the node can not be combined with other nodes return verdict = no.
    - Combine the node only to nodes that are highly similar. Just match identical nodes to the given node.
    - Do not be restricted by the type and description when combining.
    - Do not create groups. Never group nodes because that creates a more abstract node. Keep the node with the single meaning.
    - Return the indexes of all the nodes that are identical
    - Return in json

Output Format:

{{
    "response":{{
        "reasoning": ...,
        "verdict": ...,
        "node_indexes": [...]
    }}
}}
"""
