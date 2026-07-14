"""Attach an unseen herb to the frozen graph using label-free compound context."""

from __future__ import annotations

import torch


def attach_query(
    features: torch.Tensor,
    edge_index: torch.Tensor,
    relation_ids: torch.Tensor,
    query_feature: torch.Tensor,
    compound_indices: list[int],
    forward_relation_id: int,
    reverse_relation_id: int,
) -> dict:
    if not compound_indices:
        raise ValueError("FORMAL_QUERY_CONTEXT_MISSING")
    device = features.device
    query_index = features.shape[0]
    compounds = torch.tensor(compound_indices, dtype=torch.long, device=device)
    query_nodes = torch.full((len(compounds),), query_index, dtype=torch.long, device=device)
    forward = torch.stack([query_nodes, compounds])
    reverse = torch.stack([compounds, query_nodes])
    return {
        "features": torch.cat([features, query_feature.view(1, -1)], dim=0),
        "edge_index": torch.cat([edge_index, forward, reverse], dim=1),
        "relation_ids": torch.cat(
            [
                relation_ids,
                torch.full((len(compounds),), forward_relation_id, dtype=torch.long, device=device),
                torch.full((len(compounds),), reverse_relation_id, dtype=torch.long, device=device),
            ]
        ),
        "query_node_index": query_index,
        "herb_target_edge_count": 0,
        "trainable_query_id_embedding": False,
    }
