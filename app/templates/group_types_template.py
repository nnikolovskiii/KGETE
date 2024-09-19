from typing import List


def group_types_template(
        types: List[str],
) -> str:
    return f""""Node Type Grouping Task

You are a sophisticated algorithm designed to identify and group node types with identical meanings to construct a knowledge graph. Your task is to analyze the provided node types and categorize them into groups based on their semantic equivalence.

Instructions:

Carefully examine the node types and identify patterns, relationships, and similarities between them.
Group the node types into clusters where each group consists of types with identical.
Avoid creating groups that are simply connected by a conjunction (e.g., "and", "or") unless the resulting group has a clear, unified meaning.

Node Types:

{", ".join(types)}

Output Format:

{{
  "groups": [
    {{
      "description": "<brief description of the group>",
      "name": "<group name>",
      "sub_types": ["<list of sub-types>"]
    }},
    {{
      "description": "<brief description of the group>",
      "name": "<group name>",
      "sub_types": ["<list of sub-types>"]
    }}
  ]
}}
		
Important Guidelines:

Group node types with identical. If they are only similar and not identical DO NOT group them together. 
If a node type does not fit into any group, do not force it; instead, create a new group or leave it ungrouped.
Return in Json.
"""
