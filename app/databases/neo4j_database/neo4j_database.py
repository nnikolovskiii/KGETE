from typing import Any, Dict, List, Optional, Tuple
from neo4j._sync.driver import Driver
from neo4j import GraphDatabase
from pydantic import BaseModel
from neo4j.graph import Node as Neo4jNode
from dotenv import load_dotenv
import os


from app.utils.str_converter import node_relationship_to_str


class NeoNode(BaseModel):
    value: str
    type: Optional[str] = "Node"
    properties: Dict[str, Any] = {}

    def __init__(self, **data):
        super().__init__(**data)
        self.value = self.value.replace("'", "")
        self.properties["value"] = self.value
        self.type = self.type.replace(" ", "_")


class NeoRelationship(BaseModel):
    type: str
    properties: Optional[Dict[str, Any]] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.type = self.type.replace(" ", "_")
    

class Neo4jDatabase:
    driver: Driver

    def __init__(self):
        load_dotenv()
        url = os.getenv("URL")
        uri = f"bolt://{url}:7687"
        username = "neo4j"
        password = "Test09875"
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def create_node(self, node: NeoNode):
        with self.driver.session() as session:
            properties = Neo4jDatabase._transform_properties(node.properties)
            cypher_query = f"CREATE (n:`{node.type}` {{{properties}}}) RETURN n"
            session.run(cypher_query)

    def node_exists(self, node: NeoNode) -> bool:
        with self.driver.session() as session:
            label = node.type
            label_existence_query = f"CALL db.labels() YIELD label RETURN label"
            labels_result = session.run(label_existence_query)
            labels = [record["label"] for record in labels_result]

            if label not in labels:
                return False

            properties = Neo4jDatabase._transform_properties(node.properties)

            cypher_query = f"MATCH (n:`{label}` {{{properties}}}) RETURN n"
            result = session.run(cypher_query)
            return result.single() is not None

    def create_relationship(
            self,
            node1: NeoNode,
            node2: NeoNode,
            relationship: NeoRelationship,
    ):
        if not self.node_exists(node1):
            self.create_node(node1)
        if not self.node_exists(node2):
            self.create_node(node2)

        with self.driver.session() as session:
            properties1 = Neo4jDatabase._transform_properties(node1.properties)
            properties2 = Neo4jDatabase._transform_properties(node2.properties)
            relationship_prop = Neo4jDatabase._transform_properties(relationship.properties) if relationship.properties else ""

            relationship_properties_clause = f" {{{relationship_prop}}}" if relationship_prop else ""
            cypher_query = f"""
            MATCH (node1:`{node1.type}` {{{properties1}}}), (node2:`{node2.type}` {{{properties2}}})
            CREATE (node1)-[:`{relationship.type}` {relationship_properties_clause}]->(node2)
            """

            session.run(cypher_query)

    def get_neighbours(self, node_name: str) -> List[Tuple[NeoNode, NeoRelationship, NeoNode]]:
        with self.driver.session() as session:
            properties = Neo4jDatabase._transform_properties({'value': node_name})
            cypher_query = f"""
            MATCH (node:`Node` {{{properties}}})-[rel]->(neighbour)
            RETURN node, rel, neighbour
            UNION
            MATCH (neighbour)-[rel]->(node:`Node` {{{properties}}})
            RETURN neighbour, rel, node
            """

            result = session.run(cypher_query)

            neighbours = []
            for record in result:
                start_node_data = record["node"]
                relationship_data = record["rel"]
                neighbour_node_data = record["neighbour"]

                start_node = NeoNode(value=start_node_data["value"], properties=dict(start_node_data))
                relationship = NeoRelationship(type=relationship_data.type, properties=dict(relationship_data))
                neighbour_node = NeoNode(value=neighbour_node_data["value"], properties=dict(neighbour_node_data))

                neighbours.append((start_node, relationship, neighbour_node))

            return neighbours

    @staticmethod
    def _create_node_from_neo4j(neo4j_node: Neo4jNode) -> NeoNode:
        data = {
            'type': next(iter(neo4j_node.labels)),
            'properties': neo4j_node._properties
        }
        return NeoNode.model_validate(data)
    
    @staticmethod
    def _transform_properties(properties: Dict[str, Any]) -> str:
        return ", ".join(f"{key}: '{value}'" for key, value in properties.items())

    def get_unique_rel_types(self) -> List[str]:
        with self.driver.session() as session:
            cypher_query = """
            MATCH ()-[rel]->()
            RETURN DISTINCT type(rel) AS relationship_type
            """
            result = session.run(cypher_query)
            relationship_types = [record["relationship_type"] for record in result]
            return relationship_types

    def get_unique_node_types(self) -> List[str]:
        with self.driver.session() as session:
            cypher_query = """
            CALL db.labels() YIELD label
            RETURN label
            """
            result = session.run(cypher_query)
            labels = [record["label"] for record in result]
            return labels

    def get_unique_triplet_types(self) -> List[Tuple[str, str, str]]:
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
