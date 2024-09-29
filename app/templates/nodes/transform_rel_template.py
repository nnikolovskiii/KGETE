from typing import List


def transform_rel_template(
        relations: List[str],
        abstract_relations: List[str],
) -> str:
    return f""""You are an expert and transforming one type of relations to other more general types that are provided to you. Your only job is to match each
relation to the one abstract relation from the provided list of abstract relations.


Relations that need to be transformed:
[{", ".join(relations)}]

Abstract relations:
[{"\n".join(abstract_relations)}]


Instructions:
    - You must match ALL of the relations to ONLY one abstract relation.
    - Provide a short reasoning before matching.
    - Return the names of the relations identical as they are given to you.
    - Return in JSON
    
Output Format:
{{
    "response":[{{
        "reasoning": ...,
        "relation": ...,
        "abstract_relation": ...
    }}...]
}}
"""
