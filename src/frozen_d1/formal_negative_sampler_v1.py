"""Frozen deterministic per-herb 1:1 train-only negative sampler."""

from __future__ import annotations

import hashlib
import random
from collections import defaultdict


def sampler_seed(run_seed: int, epoch: int, herb_id: str) -> int:
    digest = hashlib.sha256(f"{run_seed}|{epoch}|{herb_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % (2**31 - 1) or 1


def sample_formal_negatives(train_positives, candidate_targets, run_seed: int, epoch: int):
    grouped = defaultdict(set)
    for herb, target in train_positives:
        grouped[herb].add(target)
    result = []
    for herb in sorted(grouped):
        candidates = [t for t in candidate_targets if t not in grouped[herb]]
        requested = len(grouped[herb])
        if len(candidates) < requested:
            raise RuntimeError(f"NEGATIVE_CAPACITY_DEFICIT:{herb}")
        selected = random.Random(sampler_seed(run_seed, epoch, herb)).sample(candidates, requested)
        result.extend((herb, target) for target in selected)
    if len(result) != len(set(result)) or set(result) & set(train_positives):
        raise AssertionError("Formal negative invariant failure")
    return result
