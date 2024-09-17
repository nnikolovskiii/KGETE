import os.path as osp
import torch
import torch.nn.functional as F
import torch_geometric.transforms as T
from torch_geometric.datasets import DBLP

from app.modeling.hgt_model import HGT

path = osp.join(osp.dirname(osp.realpath(__file__)), '../../data/DBLP')
# We initialize conference node features with a single one-vector as feature:
dataset = DBLP(path, transform=T.Constant(node_types='conference'))
data = dataset[0]
x_dict = data.x_dict
edge_index_dict = data.edge_index_dict
for keys in edge_index_dict.keys():
    print(edge_index_dict[keys].shape)
print(len(data.metadata()))
metadata = data.metadata()
print("lol")

# model = HGT(hidden_channels=64, out_channels=4, num_heads=2, num_layers=1)
# if torch.cuda.is_available():
#     device = torch.device('cuda')
# else:
#     device = torch.device('cpu')
# data, model = data.to(device), model.to(device)
#
# with torch.no_grad():  # Initialize lazy modules.
#     out = model(data.x_dict, data.edge_index_dict)
#
# optimizer = torch.optim.Adam(model.parameters(), lr=0.005, weight_decay=0.001)
#
#
# def train():
#     model.train()
#     optimizer.zero_grad()
#     out = model(data.x_dict, data.edge_index_dict)
#     mask = data['author'].train_mask
#     loss = F.cross_entropy(out[mask], data['author'].y[mask])
#     loss.backward()
#     optimizer.step()
#     return float(loss)
#
#
# @torch.no_grad()
# def test():
#     model.eval()
#     pred = model(data.x_dict, data.edge_index_dict).argmax(dim=-1)
#
#     accs = []
#     for split in ['train_mask', 'val_mask', 'test_mask']:
#         mask = data['author'][split]
#         acc = (pred[mask] == data['author'].y[mask]).sum() / mask.sum()
#         accs.append(float(acc))
#     return accs
#
# print(data.x_dict['author'].shape)
# print("LOOOOL")
# print(data.edge_index_dict.keys())
#
# # for epoch in range(1, 101):
# #     loss = train()
# #     train_acc, val_acc, test_acc = test()
# #     print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}, Train: {train_acc:.4f}, '
# #           f'Val: {val_acc:.4f}, Test: {test_acc:.4f}')