from neo4j.graph import Node, Relationship


def node_relationship_to_str(
        node: Node,
        relationship: Relationship
) -> str:
    return f"is connected to node '{node._properties["id"]}' of type '{next(iter(node.labels))}' with relationship '{relationship.type}'"

