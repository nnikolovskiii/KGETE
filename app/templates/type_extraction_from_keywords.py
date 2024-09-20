from typing import List


def type_extraction_from_keywords_template(
        context: str,
        keywords: List[str]
):
    return f"""You are a sophisticated algorithm designed to come up with node and relation types for graphs based on keywords and context. 

Context:
{context}

Keywords:
{str(keywords)}


Example
{{
  "node_types": {{
    "Artifact": "Represents an object of historical or cultural significance",
    "Substance": "Material with specific properties",
    "Property": "Describes characteristics or qualities of a substance or object",
    "Time Period": "Represents a specific time range or era in history",
    "Location": "A place where discoveries or events occur"
  }},
  "relation_types": {{
    "Contains": "Indicates that one entity includes or holds another entity",
    "Has Property": "Describes the relationship where an entity has a specific characteristic",
    "Discovered In": "Identifies where or when an object was found",
    "Due To": "Explains a cause-and-effect relationship"
  }},
  
  
Important instructions: 

Make the types abstract. 
Do not restrict yourself to the context and keywords, because they are just little part of the knowledge base.
Try to assume what the other parts of the knowledge base are, and with that in mind create the node and relation types.
Create as many types as you can think about. Do not limit yourself to numbers.
Do not be limited to the keywords and context.
Return in json with keys "node_types" and "relation_types"
"""
