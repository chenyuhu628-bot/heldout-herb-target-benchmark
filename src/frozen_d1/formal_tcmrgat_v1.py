"""Formal TCMRGAT: multi-head relation-specific attention with learned relation gates."""

from __future__ import annotations

import torch
from torch import nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv

from formal_model_base_v1 import FormalModelBase


class FormalTCMRGAT(FormalModelBase):
    architecture_name = "TCMRGAT"
    reads_relation_ids = True

    def __init__(self, feature_builder, hidden_dim: int, relation_count: int, layers: int = 2, dropout: float = 0.2, heads: int = 4) -> None:
        if hidden_dim % heads:
            raise ValueError("hidden_dim must be divisible by attention heads")
        super().__init__(feature_builder, hidden_dim, relation_count, layers, dropout)
        self.heads = heads
        self.relation_layers = nn.ModuleList(
            [
                nn.ModuleList(
                    [
                        GATConv(hidden_dim, hidden_dim // heads, heads=heads, concat=True, dropout=dropout, add_self_loops=False)
                        for _ in range(relation_count)
                    ]
                )
                for _ in range(layers)
            ]
        )
        self.relation_gates = nn.ParameterList([nn.Parameter(torch.zeros(relation_count)) for _ in range(layers)])
        self.residual_alpha = nn.ParameterList([nn.Parameter(torch.tensor(0.0)) for _ in range(layers)])
        self.norms = nn.ModuleList([nn.LayerNorm(hidden_dim) for _ in range(layers)])

    def _encode(self, x, edge_index, relation_ids):
        for layer_index, relation_modules in enumerate(self.relation_layers):
            aggregate = torch.zeros_like(x)
            for relation_id, module in enumerate(relation_modules):
                mask = relation_ids == relation_id
                if torch.any(mask):
                    message = module(x, edge_index[:, mask])
                    aggregate = aggregate + torch.sigmoid(self.relation_gates[layer_index][relation_id]) * message
            update = F.dropout(F.relu(aggregate), p=self.dropout_rate, training=self.training)
            x = self.norms[layer_index](x + torch.sigmoid(self.residual_alpha[layer_index]) * update)
        return x

    def architecture_config(self):
        return {**super().architecture_config(), "attention_heads": self.heads, "evidence_stratified_relations": True, "relation_gates": True}
