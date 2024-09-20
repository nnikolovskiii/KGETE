from typing import List, Optional


def extract_triplets_template(
        text: str,
        node_types: Optional[List[str]] = None,
        rel_types: Optional[List[str]] = None,
) -> str:
    return f"""### Instructions

1. **Node and Relation Types**:
   - **Node Types**: [Define the types of nodes present in the text]
     - **General Definition**: [Provide a brief general definition for each node type]
   - **Relation Types**: [Define the types of relationships between the nodes]
     - **General Definition**: [Provide a brief general definition for each relation type]

2. **Triplets**:
   - **(Node: A) - [Relation] → (Node: B)**
   - **(Node: C) - [Relation] → (Node: D)**

---

### Example

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
  "triplets": [
  {{
    "head_type": "Artifact",
    "head_value": "Pots of Honey",
    "relation": "Discovered In",
    "tail_type": "Location",
    "tail_value": "Ancient Egyptian Tombs"
  }},
  {{
    "head_type": "Artifact",
    "head_value": "Pots of Honey",
    "relation": "Has Property",
    "tail_type": "Property",
    "tail_value": "Edible"
  }},
  {{
    "head_type": "Artifact",
    "head_value": "Pots of Honey",
    "relation": "Has Property",
    "tail_type": "Time Period",
    "tail_value": "Over 3,000 years old"
  }},
  {{
    "head_type": "Substance",
    "head_value": "Honey",
    "relation": "Has Property",
    "tail_type": "Property",
    "tail_value": "Long Shelf Life"
  }},
  {{
    "head_type": "Property",
    "head_value": "Long Shelf Life",
    "relation": "Due To",
    "tail_type": "Property",
    "tail_value": "Unique Composition"
  }},
  {{
    "head_type": "Property",
    "head_value": "Unique Composition",
    "relation": "Contains",
    "tail_type": "Substance",
    "tail_value": "Acidic"
  }}
]
}}


---

### Text:
{text}

---


### Important instructions
    - Create simple and abstract node and relationship types. Create simple and abstract triplets.
    - The values of the triplets need to be not too long, and consisting of a single thing.
    - Return in json
"""
