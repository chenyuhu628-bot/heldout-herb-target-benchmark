"""Formal feature contract: shared trainable non-herb embeddings and context-only herbs."""

from __future__ import annotations

import torch
from torch import nn


class FormalFeatureBuilder(nn.Module):
    """No herb-ID parameters; every herb is the mean of its compound embeddings."""

    uses_id_hash = False
    has_trainable_herb_id_embedding = False

    def __init__(
        self,
        num_nodes: int,
        compound_global_indices: list[int],
        target_global_indices: list[int],
        herb_context: dict[int, list[int]],
        hidden_dim: int,
    ) -> None:
        super().__init__()
        self.num_nodes = num_nodes
        self.hidden_dim = hidden_dim
        self.compound_embedding = nn.Embedding(len(compound_global_indices), hidden_dim)
        self.target_embedding = nn.Embedding(len(target_global_indices), hidden_dim)
        nn.init.xavier_uniform_(self.compound_embedding.weight)
        nn.init.xavier_uniform_(self.target_embedding.weight)
        compound_lookup = torch.full((num_nodes,), -1, dtype=torch.long)
        target_lookup = torch.full((num_nodes,), -1, dtype=torch.long)
        compound_lookup[torch.tensor(compound_global_indices)] = torch.arange(len(compound_global_indices))
        target_lookup[torch.tensor(target_global_indices)] = torch.arange(len(target_global_indices))
        self.register_buffer("compound_global_to_local", compound_lookup)
        self.register_buffer("target_global_to_local", target_lookup)
        self.herb_context = {int(k): [int(v) for v in values] for k, values in herb_context.items()}

    def encode_compound_context(self, compound_global_indices: list[int]) -> torch.Tensor:
        if not compound_global_indices:
            raise ValueError("FORMAL_HERB_CONTEXT_MISSING")
        global_index = torch.tensor(
            compound_global_indices,
            dtype=torch.long,
            device=self.compound_global_to_local.device,
        )
        local_index = self.compound_global_to_local[global_index]
        if torch.any(local_index < 0):
            raise ValueError("Herb context contains a non-compound endpoint")
        return self.compound_embedding(local_index).mean(dim=0)

    def build_training_features(self) -> torch.Tensor:
        device = self.compound_embedding.weight.device
        x = torch.zeros((self.num_nodes, self.hidden_dim), device=device)
        compound_global = torch.where(self.compound_global_to_local >= 0)[0]
        target_global = torch.where(self.target_global_to_local >= 0)[0]
        x[compound_global] = self.compound_embedding(self.compound_global_to_local[compound_global])
        x[target_global] = self.target_embedding(self.target_global_to_local[target_global])
        for herb_global, compounds in self.herb_context.items():
            x[herb_global] = self.encode_compound_context(compounds)
        return x

    def feature_contract(self) -> dict:
        return {
            "herb": "mean of shared compound embeddings over label-free herb-compound context",
            "compound": "shared trainable transductive embedding",
            "target": "shared trainable transductive embedding",
            "query_herb": "same compound-context mean function used for train herbs",
            "missing_herb_context": "hard error",
            "uses_id_hash": False,
            "trainable_herb_id_embedding": False,
            "hidden_dim": self.hidden_dim,
        }
