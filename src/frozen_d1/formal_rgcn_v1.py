"""Formal RGCN baseline with frozen relation count and basis decomposition."""

from torch import nn
import torch.nn.functional as F
from torch_geometric.nn import RGCNConv

from formal_model_base_v1 import FormalModelBase


class FormalRGCN(FormalModelBase):
    architecture_name = "RGCN"
    reads_relation_ids = True

    def __init__(self, feature_builder, hidden_dim, relation_count, layers=2, dropout=0.2, num_bases=None):
        super().__init__(feature_builder, hidden_dim, relation_count, layers, dropout)
        self.num_bases = min(4, relation_count) if num_bases is None else num_bases
        self.layers = nn.ModuleList(
            [RGCNConv(hidden_dim, hidden_dim, relation_count, num_bases=self.num_bases) for _ in range(layers)]
        )
        self.norms = nn.ModuleList([nn.LayerNorm(hidden_dim) for _ in range(layers)])

    def _encode(self, x, edge_index, relation_ids):
        for layer, norm in zip(self.layers, self.norms):
            x = norm(x + F.dropout(F.relu(layer(x, edge_index, relation_ids)), p=self.dropout_rate, training=self.training))
        return x

    def architecture_config(self):
        return {**super().architecture_config(), "num_bases": self.num_bases}
