from typing import List, Dict, Tuple

import torch
from torch_geometric.nn.conv import GATConv
import torch.nn.functional as F
from torch import Tensor
from pydantic import BaseModel

Relation = Tuple[str, str, str]
Node = str


class CustomHeteroMetadata(BaseModel):
    num_all_nodes: int
    node_types: List[Node]
    num_node_types_dict: Dict[str, int]
    rel_types: List[Relation]

    def metadata(self) -> Tuple[List[str], List[Relation]]:
        return self.node_types, self.rel_types


class GNN(torch.nn.Module):
    def __init__(
            self,
            metadata: CustomHeteroMetadata,
            num_layers: int,
            hidden_channels: int
    ) -> None:
        super().__init__()
        self.metadata = metadata
        self.num_layers = num_layers
        self.hidden_channels = hidden_channels
        self.convs: Dict[Relation, List[torch.nn.Module]] = {}
        self.embeddings = torch.nn.Embedding(num_embeddings=metadata.num_all_nodes, embedding_dim=hidden_channels)

        for rel_type in metadata.rel_types:
            self.convs[rel_type] = [GATConv(in_channels=hidden_channels, out_channels=hidden_channels) for layer in
                                    num_layers]

        # interaction part
        for int_rel_type in [("interaction", "interacts", "node"), ("node", "interacts", "interaction")]:
            self.convs[int_rel_type] = [GATConv(in_channels=hidden_channels, out_channels=hidden_channels) for layer in
                                        num_layers]

    def forward(self, edge_index_dict: Dict[Relation, Tensor]) -> Tensor:
        for rel_type in self.metadata.rel_types:
            if rel_type in edge_index_dict:
                edge_index = edge_index_dict[rel_type]
                new_edge_index = []
                x = []
                node_ids_dict = {}
                linear_tensor = edge_index.flatten()
                for node_id in linear_tensor:
                    if node_id not in node_ids_dict:
                        node_ids_dict[node_id] = len(node_ids_dict)
                        x.append(self.embeddings(node_id))
                    new_edge_index.append(node_ids_dict[node_id])

                x = torch.cat(x, dim=-1)
                new_edge_index = torch.tensor(new_edge_index, dtype=torch.long).reshape(2, -1)

                for layer in self.convs[rel_type][:-1]:
                    x = F.relu(layer(x, new_edge_index))

                x = self.convs[rel_type][-1](x, new_edge_index)

