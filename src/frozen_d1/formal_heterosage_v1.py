"""Formal relation-separated HeteroSAGE without attention."""

import torch
from torch import nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

from formal_model_base_v1 import FormalModelBase


class FormalHeteroSAGE(FormalModelBase):
    architecture_name = "HeteroSAGE"
    reads_relation_ids = True

    def __init__(self, feature_builder, hidden_dim, relation_count, layers=2, dropout=0.2):
        super().__init__(feature_builder, hidden_dim, relation_count, layers, dropout)
        self.relation_layers = nn.ModuleList(
            [nn.ModuleList([SAGEConv(hidden_dim, hidden_dim) for _ in range(relation_count)]) for _ in range(layers)]
        )
        self.norms = nn.ModuleList([nn.LayerNorm(hidden_dim) for _ in range(layers)])

    def _encode(self, x, edge_index, relation_ids):
        for layer_index, modules in enumerate(self.relation_layers):
            messages = []
            for relation_id, module in enumerate(modules):
                mask = relation_ids == relation_id
                if torch.any(mask):
                    messages.append(module(x, edge_index[:, mask]))
            aggregate = torch.stack(messages).mean(0) if messages else torch.zeros_like(x)
            x = self.norms[layer_index](x + F.dropout(F.relu(aggregate), p=self.dropout_rate, training=self.training))
        return x
