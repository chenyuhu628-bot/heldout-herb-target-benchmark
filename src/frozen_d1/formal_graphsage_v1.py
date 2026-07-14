"""Formal homogeneous GraphSAGE baseline using collapsed allowed context arcs."""

from torch import nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

from formal_model_base_v1 import FormalModelBase


class FormalGraphSAGE(FormalModelBase):
    architecture_name = "GraphSAGE"
    reads_relation_ids = False

    def __init__(self, feature_builder, hidden_dim, relation_count, layers=2, dropout=0.2):
        super().__init__(feature_builder, hidden_dim, relation_count, layers, dropout)
        self.layers = nn.ModuleList([SAGEConv(hidden_dim, hidden_dim) for _ in range(layers)])
        self.norms = nn.ModuleList([nn.LayerNorm(hidden_dim) for _ in range(layers)])

    def _encode(self, x, edge_index, relation_ids):
        for layer, norm in zip(self.layers, self.norms):
            x = norm(x + F.dropout(F.relu(layer(x, edge_index)), p=self.dropout_rate, training=self.training))
        return x
