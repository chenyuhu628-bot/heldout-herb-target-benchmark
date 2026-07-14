"""Unified formal interface shared by all five model families."""

from __future__ import annotations

from abc import ABC, abstractmethod

import torch
from torch import nn

from formal_feature_builder_v1 import FormalFeatureBuilder
from formal_pair_decoder_v1 import FormalPairDecoder
from formal_query_adapter_v1 import attach_query


class FormalModelBase(nn.Module, ABC):
    reads_relation_ids = True
    architecture_name = "BASE"

    def __init__(self, feature_builder: FormalFeatureBuilder, hidden_dim: int, relation_count: int, layers: int, dropout: float) -> None:
        super().__init__()
        self.feature_builder = feature_builder
        self.hidden_dim = hidden_dim
        self.relation_count = relation_count
        self.layer_count = layers
        self.dropout_rate = dropout
        self.decoder = FormalPairDecoder(hidden_dim)

    @abstractmethod
    def _encode(self, x: torch.Tensor, edge_index: torch.Tensor, relation_ids: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

    def encode_training_graph(self, edge_index: torch.Tensor, relation_ids: torch.Tensor) -> torch.Tensor:
        return self._encode(self.feature_builder.build_training_features(), edge_index, relation_ids)

    def encode_query_herb(
        self,
        edge_index: torch.Tensor,
        relation_ids: torch.Tensor,
        compound_indices: list[int],
        forward_relation_id: int,
        reverse_relation_id: int,
    ) -> tuple[torch.Tensor, int]:
        features = self.feature_builder.build_training_features()
        query_feature = self.feature_builder.encode_compound_context(compound_indices)
        query = attach_query(
            features,
            edge_index,
            relation_ids,
            query_feature,
            compound_indices,
            forward_relation_id,
            reverse_relation_id,
        )
        return self._encode(query["features"], query["edge_index"], query["relation_ids"]), query["query_node_index"]

    def score_pairs(self, z: torch.Tensor, herb_indices: torch.Tensor, target_indices: torch.Tensor) -> torch.Tensor:
        return self.decoder(z[herb_indices], z[target_indices])

    def parameter_count(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def architecture_config(self) -> dict:
        return {
            "model": self.architecture_name,
            "hidden_dim": self.hidden_dim,
            "layers": self.layer_count,
            "dropout": self.dropout_rate,
            "relation_count": self.relation_count,
            "reads_relation_ids": self.reads_relation_ids,
            "trainable_herb_id_embedding": False,
            "decoder": "FormalPairDecoderV1",
        }
