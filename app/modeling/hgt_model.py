from typing import List, Tuple, Dict
from pydantic import BaseModel
import torch
from torch_geometric.nn import HGTConv, Linear


class GraphMetadata(BaseModel):
    node_types: List[str]
    edge_types: List[Tuple[str,str,str]]
    num_nodes_dict: Dict[str, int]


class HGT(torch.nn.Module):
    def __init__(
            self,
            hidden_channels: int,
            out_channels: int,
            num_heads: int,
            num_layers: int,
            graph_metadata: GraphMetadata,
    ):
        super().__init__()

        self.lin_dict = torch.nn.ModuleDict()
        for node_type in graph_metadata.node_types:
            self.lin_dict[node_type] = Linear(-1, hidden_channels)

        self.embeddings_layers = torch.nn.ModuleDict()

        for node_type in graph_metadata.node_types:
            self.embeddings_layers[node_type] = torch.nn.Embedding(graph_metadata.num_nodes_dict[node_type], hidden_channels)

        self.convs = torch.nn.ModuleList()
        for _ in range(num_layers):
            conv = HGTConv(
                in_channels=hidden_channels,
                out_channels=hidden_channels,
                metadata=(graph_metadata.node_types, graph_metadata.edge_types),
                heads=num_heads)
            self.convs.append(conv)

        self.lin = Linear(hidden_channels, out_channels)

    def forward(self, x_dict, edge_index_dict):
        x_dict = {
            node_type: self.lin_dict[node_type](x).relu_()
            for node_type, x in x_dict.items()
        }

        for conv in self.convs:
            x_dict = conv(x_dict, edge_index_dict)

        return None