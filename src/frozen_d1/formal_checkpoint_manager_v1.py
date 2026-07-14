"""Formal checkpoint metadata and reload guard."""

from __future__ import annotations

from pathlib import Path
import torch


REQUIRED_METADATA = {
    "formal_protocol_version",
    "model_name",
    "config_id",
    "config_hash",
    "run_seed",
    "input_hashes",
    "code_version",
}


def save_checkpoint(path: Path, model, metadata: dict) -> None:
    missing = REQUIRED_METADATA - set(metadata)
    if missing:
        raise ValueError(f"FORMAL_CHECKPOINT_METADATA_MISSING:{sorted(missing)}")
    torch.save({"state_dict": model.state_dict(), "metadata": metadata}, path)


def load_checkpoint(path: Path, model, expected_config_hash: str) -> dict:
    if "checkpoints_nonformal_smoke" in str(path).casefold():
        raise PermissionError("C3_SMOKE_CHECKPOINT_REUSE_FORBIDDEN")
    payload = torch.load(path, map_location="cpu", weights_only=True)
    metadata = payload.get("metadata", {})
    missing = REQUIRED_METADATA - set(metadata)
    if missing:
        raise ValueError("FORMAL_CHECKPOINT_METADATA_MISSING")
    if metadata["config_hash"] != expected_config_hash:
        raise ValueError("FORMAL_CHECKPOINT_CONFIG_HASH_MISMATCH")
    model.load_state_dict(payload["state_dict"])
    return metadata
