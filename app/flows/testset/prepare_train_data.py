from typing import List, Dict, Tuple

import torch
from pydantic import BaseModel

from app.databases.neo4j_database.neo4j_database import Neo4jDataset
from app.modeling.hgt_model import GraphMetadata, Edge


class Graph(BaseModel):
    node_ids_dict: Dict[str, int]
    edge_index_dict: Dict[Edge, torch.Tensor] # [2, *]


chunks: List[str]


def connect_int_node(local_graph: Graph) -> None:
    node_types = local_graph.node_ids_dict.keys()
    for node_type in node_types:
        node_ids = local_graph.node_ids_dict[node_type]
        node_ids_tensor = torch.tensor(node_ids)

        # may need improvements
        int_edge_away = Edge(from_node_type="int_node", rel_type="Interaction", to_node_type="node_type")
        int_edge_towards = Edge(from_node_type="node_type", rel_type="Interaction", to_node_type="int_node")

        zero_row = torch.zeros_like(node_ids_tensor)

        local_graph.edge_index_dict[int_edge_away] = torch.stack([zero_row, node_ids_tensor])
        local_graph.edge_index_dict[int_edge_towards] = torch.stack([node_ids_tensor, zero_row])


nd = Neo4jDataset()
node_types = nd.get_all_unique_node_types()
node_types.append("int_node")
edge_types = nd.get_all_edge_types()
edge_types.append()
num_nodes_dict = {}

chunk_graph_pairs = []

for node_type in node_types:
    num_nodes = nd.get_num_nodes(node_type=node_type)
    num_nodes_dict[node_type] = num_nodes

for chunk in chunks:
    local_graph:Graph = get_local_graph(context=chunk)

    #connect an interaction node to the local graph
    connect_int_node(local_graph)

    chunk_graph_pair = ChunkGraphPair(chunk=chunk, local_graph=local_graph)
    chunk_graph_pairs.append(chunk_graph_pair)


GraphMetadata(node_types=node_types, edge_types=edge_types, num_nodes_dict=num_nodes_dict)





