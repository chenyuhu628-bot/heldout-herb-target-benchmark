"""Shared pair decoder contract for every formal model."""

from __future__ import annotations

import torch
from torch import nn


class FormalPairDecoder(nn.Module):
    def __init__(self, hidden_dim: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(hidden_dim * 4, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, herb: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        pair = torch.cat([herb, target, herb * target, torch.abs(herb - target)], dim=-1)
        return self.network(pair).squeeze(-1)

    def parameter_count(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
