from typing import List, Dict, Tuple

import torch
from torch_geometric.nn.conv import GATConv
import torch.nn.functional as F
from torch import Tensor
from torch_geometric.data import HeteroData
from torch_geometric.nn import to_hetero
from pydantic import BaseModel


class CustomHeteroData(BaseModel):
    node_types: List[str]
    num_node_types_dict: Dict[str, int]
    rel_types: List[Tuple[str, str, str]]

    def metadata(self) -> Tuple[List[str], List[Tuple[str, str, str]]]:
        return self.node_types, self.rel_types


class GNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = GATConv(hidden_channels, hidden_channels)
        self.conv2 = GATConv(hidden_channels, hidden_channels)

    def forward(self, x: Tensor, edge_index: Tensor) -> Tensor:
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x


class Classifier(torch.nn.Module):
    def forward(self, x_user: Tensor, x_movie: Tensor, edge_label_index: Tensor) -> Tensor:
        edge_feat_user = x_user[edge_label_index[0]]
        edge_feat_movie = x_movie[edge_label_index[1]]

        return (edge_feat_user * edge_feat_movie).sum(dim=-1)


class Model(torch.nn.Module):
    def __init__(self, data: CustomHeteroData, hidden_channels: int) -> None:
        super().__init__()
        self.embeddings_layers = torch.nn.ModuleDict()

        for node_type in data.node_types:
            self.embeddings_layers[node_type] = torch.nn.Embedding(
                num_embeddings=data.num_node_types_dict[node_type],
                embedding_dim=hidden_channels)

        self.gnn = GNN(hidden_channels)
        self.gnn = to_hetero(self.gnn, metadata=data.metadata())
        self.classifier = Classifier()

    def forward(self, data: CustomHeteroData) -> Tensor:
        x_dict = {
            node_type: self.embeddings_layers[node_type](data[node_type].node_id)
            for node_type in data.node_types}

        x_dict = self.gnn(x_dict, data.edge_index_dict)

        return None


model = Model(hidden_channels=64)
