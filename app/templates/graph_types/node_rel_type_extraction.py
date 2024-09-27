def node_rel_type_extraction_template(
        text: str
):
    return f"""You are a top-tier algorithm designed for extracting information in structured formats to build a knowledge graph. Your task is given a text to extract node types and relationship types.
Make the node types as simple and general as possible.

Example 1:
Input: Adam is a software engineer in Microsoft since 2009. Microsoft is a tech company that provide several products such as Microsoft Word. Microsoft Word is a lightweight app that accessible offline

Output:
{{"node_types": ["Person, Company, Product, Characteristic"],
"rel_types": ["WORKS_FOR", "PRODUCED_BY", "HAS_CHARACTERISTIC"]}}

Text:
{text}

Return in JSON format with keys "node_types" and "rel_types"."""
