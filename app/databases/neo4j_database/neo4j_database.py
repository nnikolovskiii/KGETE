from typing import Any, Dict, List, Optional, Tuple
from neo4j._sync.driver import Driver
from neo4j import GraphDatabase
from pydantic import BaseModel
from neo4j.graph import Node as Neo4jNode

from app.utils.str_converter import node_relationship_to_str


class Node(BaseModel):
    type: str
    properties: Dict[str, Any]
    
    
class Relationship(BaseModel):
    type: str
    properties: Optional[Dict[str, Any]] = None
    

class Neo4jDataset:
    driver: Driver

    def __init__(self):
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "Test09875"
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def create_node(self, node: Node):
        with self.driver.session() as session:
            if not self.node_exists(node):
                properties = Neo4jDataset._transform_properties(node.properties)
                cypher_query = f"CREATE (n:`{node.type}` {{{properties}}}) RETURN n"
                session.run(cypher_query)

    def node_exists(self, node: Node) -> bool:
        with self.driver.session() as session:
            label = node.type
            label_existence_query = f"CALL db.labels() YIELD label RETURN label"
            labels_result = session.run(label_existence_query)
            labels = [record["label"] for record in labels_result]

            if label not in labels:
                return False

            properties = Neo4jDataset._transform_properties(node.properties)
            cypher_query = f"MATCH (n:`{label}` {{{properties}}}) RETURN n"
            result = session.run(cypher_query)
            return result.single() is not None

    def create_relationship(
            self,
            node1: Node,
            node2: Node,
            relationship: Relationship,
    ):
        if not self.node_exists(node1):
            self.create_node(node1)
        if not self.node_exists(node2):
            self.create_node(node2)

        with self.driver.session() as session:
            properties1 = Neo4jDataset._transform_properties(node1.properties)
            properties2 = Neo4jDataset._transform_properties(node2.properties)
            relationship_prop = Neo4jDataset._transform_properties(relationship.properties) if relationship.properties else ""

            relationship_properties_clause = f" {{{relationship_prop}}}" if relationship_prop else ""
            cypher_query = f"""
            MATCH (node1:`{node1.type}` {{{properties1}}}), (node2:`{node2.type}` {{{properties2}}})
            CREATE (node1)-[:{relationship.type}{relationship_properties_clause}]->(node2)
            """

            session.run(cypher_query)

    def get_neighbours(
            self,
            node_type: str,
            node_prop: Dict[str, Any]
    ) -> str:
        with self.driver.session() as session:
            properties = Neo4jDataset._transform_properties(node_prop)
            cypher_query = f"""
            MATCH (node:`{node_type}` {{{properties}}})-[rel]->(neighbour)
            RETURN neighbour, rel
            UNION
            MATCH (neighbour)-[rel]->(node:`{node_type}` {{{properties}}})
            RETURN neighbour, rel
            """

            result = session.run(cypher_query)

            return f"Value: {node_prop["id"]}\n" + "\n".join(
                [node_relationship_to_str(node, relationship) for node, relationship in result])

    @staticmethod
    def _create_node_from_neo4j(neo4j_node: Neo4jNode) -> Node:
        data = {
            'type': next(iter(neo4j_node.labels)),
            'properties': neo4j_node._properties
        }
        return Node.model_validate(data)
    
    @staticmethod
    def _transform_properties(properties: Dict[str, Any]) -> str:
        return ", ".join(f"{key}: '{value}'" for key, value in properties.items())

    def get_all_unique_node_types(self) -> List[str]:
        with self.driver.session() as session:
            cypher_query = """
            CALL db.labels() YIELD label
            RETURN label
            """
            result = session.run(cypher_query)
            labels = [record["label"] for record in result]
            return labels

    def get_all_unique_relationship_types(self) -> List[Tuple[str, str, str]]:
        with self.driver.session() as session:
            cypher_query = """
            MATCH (src)-[rel]->(dest)
            RETURN DISTINCT labels(src) AS src_node_type, type(rel) AS relationship_type, labels(dest) AS dest_node_type
            """
            result = session.run(cypher_query)

            unique_relationship_types = [
                (src_node_type[0], relationship_type, dest_node_type[0])
                for record in result
                for src_node_type in [record["src_node_type"]]
                for dest_node_type in [record["dest_node_type"]]
                for relationship_type in [record["relationship_type"]]
            ]
            return unique_relationship_types
