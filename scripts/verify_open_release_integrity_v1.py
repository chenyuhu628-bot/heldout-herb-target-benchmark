#!/usr/bin/env python3
"""Verify the public fixed-test assets without retraining or inference."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import torch


EXPECTED_MODELS = {"GCN", "GraphSAGE", "HeteroSAGE", "RGCN", "TCMRGAT"}
EXPECTED_CHECKPOINTS = 25
EXPECTED_TEST_HERBS = 67
EXPECTED_TARGETS = 2309
EXPECTED_TEST_PAIRS = 8632
EXPECTED_COMPARISONS = 275
WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def fail(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def scalar_text(value: Any) -> str:
    if isinstance(value, np.ndarray):
        return str(value.item())
    return str(value)


def state_dict_sha256(state_dict: dict[str, Any]) -> str:
    digest = hashlib.sha256()
    for key in sorted(state_dict):
        value = state_dict[key]
        digest.update(key.encode("utf-8"))
        if isinstance(value, torch.Tensor):
            tensor = value.detach().cpu().contiguous()
            digest.update(str(tensor.dtype).encode("utf-8"))
            digest.update(json.dumps(list(tensor.shape)).encode("utf-8"))
            digest.update(tensor.reshape(-1).view(torch.uint8).numpy().tobytes())
        else:
            digest.update(repr(value).encode("utf-8"))
    return digest.hexdigest()


def metadata_contains_local_path(value: Any) -> bool:
    if isinstance(value, dict):
        return any(
            (
                isinstance(key, str)
                and (WINDOWS_ABSOLUTE.match(key) or "file:///" in key)
            )
            or metadata_contains_local_path(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple)):
        return any(metadata_contains_local_path(item) for item in value)
    return isinstance(value, str) and (
        WINDOWS_ABSOLUTE.match(value) is not None or "file:///" in value
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify fixed public assets and score archive integrity without GPU inference."
    )
    parser.add_argument(
        "--package-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.package_root.resolve()
    errors: list[str] = []

    label_manifest_path = root / "data/labels/test_label_release_manifest_v1.json"
    label_manifest = json.loads(label_manifest_path.read_text(encoding="utf-8"))
    label_files = label_manifest["test_label_files"]
    herb_path = root / "data/labels/test_positive_herbs_v1.csv"
    pair_path = root / "data/labels/test_positive_pairs_v1.csv"
    herb_rows = read_csv(herb_path)
    pair_rows = read_csv(pair_path)
    herb_ids = [row["herb_id"] for row in herb_rows]
    fail(errors, len(herb_ids) == EXPECTED_TEST_HERBS, "Expected 67 public test herbs.")
    fail(errors, len(set(herb_ids)) == EXPECTED_TEST_HERBS, "Public test herb IDs are not unique.")
    fail(errors, len(pair_rows) == EXPECTED_TEST_PAIRS, "Expected 8,632 public test pairs.")
    fail(
        errors,
        sha256_file(herb_path) == label_files["test_positive_herbs_v1.csv"],
        "Test-herb file SHA-256 differs from label manifest.",
    )
    fail(
        errors,
        sha256_file(pair_path) == label_files["test_positive_pairs_v1.csv"],
        "Test-pair file SHA-256 differs from label manifest.",
    )

    candidate_rows = read_csv(root / "data/graph/candidate_target_universe_v1.csv")
    target_ids = [row["target_id"] for row in candidate_rows]
    fail(errors, len(target_ids) == EXPECTED_TARGETS, "Expected 2,309 candidate targets.")
    fail(errors, len(set(target_ids)) == EXPECTED_TARGETS, "Candidate target IDs are not unique.")
    fail(
        errors,
        [int(row["candidate_order"]) for row in candidate_rows] == list(range(EXPECTED_TARGETS)),
        "Candidate target order is not the required 0 through 2,308 sequence.",
    )

    checkpoints = read_csv(root / "artifacts/checkpoints/checkpoint_manifest_v1.csv")
    sanitization_path = root / "data/provenance/checkpoint_metadata_path_sanitization_v1.json"
    sanitization = json.loads(sanitization_path.read_text(encoding="utf-8"))
    sanitization_records = {
        str(item["run_id"]): item for item in sanitization.get("records", [])
    }
    model_counts = Counter(row["model"] for row in checkpoints)
    fail(errors, len(checkpoints) == EXPECTED_CHECKPOINTS, "Expected 25 fixed checkpoints.")
    fail(errors, set(model_counts) == EXPECTED_MODELS, "Checkpoint manifest model set is incorrect.")
    fail(
        errors,
        all(model_counts[model] == 5 for model in EXPECTED_MODELS),
        "Each model must have five fixed final checkpoints.",
    )
    checkpoint_by_run = {row["run_id"]: row for row in checkpoints}
    fail(
        errors,
        len(checkpoint_by_run) == EXPECTED_CHECKPOINTS,
        "Checkpoint run IDs are not unique.",
    )
    fail(
        errors,
        sanitization.get("checkpoint_count") == EXPECTED_CHECKPOINTS,
        "Checkpoint metadata sanitization record does not describe 25 checkpoints.",
    )
    fail(
        errors,
        set(sanitization_records) == set(checkpoint_by_run),
        "Checkpoint metadata sanitization run IDs do not match checkpoint manifest.",
    )
    for row in checkpoints:
        relative = Path(row["relative_path"])
        fail(errors, not relative.is_absolute() and ".." not in relative.parts, f"Unsafe checkpoint path: {relative}")
        checkpoint_path = root / relative
        fail(errors, checkpoint_path.is_file(), f"Missing checkpoint: {relative}")
        if checkpoint_path.is_file():
            fail(
                errors,
                checkpoint_path.stat().st_size == int(row["size_bytes"]),
                f"Checkpoint size mismatch: {relative}",
            )
            fail(
                errors,
                sha256_file(checkpoint_path) == row["sha256"],
                f"Checkpoint SHA-256 mismatch: {relative}",
            )
            checkpoint_payload = torch.load(
                checkpoint_path, map_location="cpu", weights_only=True
            )
            checkpoint_metadata = checkpoint_payload.get("metadata", {})
            fail(
                errors,
                not metadata_contains_local_path(checkpoint_metadata),
                f"Checkpoint metadata contains a machine-local path: {relative}",
            )
            sanitization_record = sanitization_records.get(row["run_id"], {})
            fail(
                errors,
                sanitization_record.get("released_checkpoint_sha256") == row["sha256"],
                f"Checkpoint sanitization provenance SHA-256 mismatch: {relative}",
            )
            fail(
                errors,
                bool(sanitization_record.get("state_dict_sha256")),
                f"Checkpoint sanitization provenance lacks state_dict fingerprint: {relative}",
            )
            fail(
                errors,
                state_dict_sha256(checkpoint_payload["state_dict"])
                == sanitization_record.get("state_dict_sha256"),
                f"Checkpoint state_dict fingerprint mismatch: {relative}",
            )

    export_manifest = json.loads(
        (root / "results/metrics/open_frozen_score_export_manifest_v1.json").read_text(
            encoding="utf-8"
        )
    )
    fail(errors, export_manifest.get("historical_metric_match") is True, "Historical metric match is not true.")
    fail(errors, export_manifest.get("retraining_performed") is False, "Release manifest reports retraining.")
    fail(
        errors,
        export_manifest.get("model_reselection_performed") is False,
        "Release manifest reports model reselection.",
    )
    score_artifacts = export_manifest.get("score_artifacts", [])
    fail(errors, len(score_artifacts) == EXPECTED_CHECKPOINTS, "Expected 25 score artifacts.")

    score_runs: set[str] = set()
    for item in score_artifacts:
        relative = Path(item["relative_path"])
        score_path = root / relative
        run_id = str(item["run_id"])
        score_runs.add(run_id)
        fail(errors, score_path.is_file(), f"Missing score matrix: {relative}")
        if not score_path.is_file():
            continue
        fail(
            errors,
            sha256_file(score_path) == item["sha256"],
            f"Score matrix SHA-256 mismatch: {relative}",
        )
        with np.load(score_path, allow_pickle=False) as archive:
            required = {"scores", "herb_ids", "target_ids", "metadata_json"}
            fail(
                errors,
                required.issubset(set(archive.files)),
                f"Score matrix lacks required arrays: {relative}",
            )
            if required.issubset(set(archive.files)):
                scores = archive["scores"]
                observed_herbs = [str(value) for value in archive["herb_ids"].tolist()]
                observed_targets = [str(value) for value in archive["target_ids"].tolist()]
                fail(
                    errors,
                    scores.shape == (EXPECTED_TEST_HERBS, EXPECTED_TARGETS),
                    f"Unexpected score shape in {relative}: {scores.shape}",
                )
                fail(
                    errors,
                    observed_herbs == herb_ids,
                    f"Herb axis differs from public fixed axis: {relative}",
                )
                fail(
                    errors,
                    observed_targets == target_ids,
                    f"Target axis differs from public fixed axis: {relative}",
                )
                metadata = json.loads(scalar_text(archive["metadata_json"]))
                fail(
                    errors,
                    not metadata_contains_local_path(metadata),
                    f"Score metadata contains a machine-local path: {relative}",
                )
                fail(
                    errors,
                    metadata.get("run_id") == run_id,
                    f"Score metadata run ID mismatch: {relative}",
                )
                fail(
                    errors,
                    metadata.get("score_semantics")
                    == "raw_decoder_logits; not calibrated probabilities",
                    f"Score semantics mismatch: {relative}",
                )
                fail(
                    errors,
                    metadata.get("public_fixed_test") is True,
                    f"Score metadata does not mark public fixed test: {relative}",
                )

    fail(
        errors,
        score_runs == set(checkpoint_by_run),
        "Score archive run IDs do not exactly match checkpoint manifest run IDs.",
    )

    comparison_rows = read_csv(
        root / "results/metrics/historical_metric_reproduction_comparison_v1.csv"
    )
    fail(
        errors,
        len(comparison_rows) == EXPECTED_COMPARISONS,
        "Expected 275 historical metric comparisons.",
    )
    fail(
        errors,
        all(row["within_tolerance"] == "True" for row in comparison_rows),
        "At least one historical metric comparison falls outside tolerance.",
    )

    report = {
        "version": "open_release_integrity_verification_v1",
        "passed": not errors,
        "error_count": len(errors),
        "errors": errors,
        "test_herb_count": len(herb_ids),
        "recorded_positive_pair_count": len(pair_rows),
        "candidate_target_count": len(target_ids),
        "checkpoint_count": len(checkpoints),
        "checkpoint_metadata_paths_redacted": not any(
            "machine-local path" in error for error in errors
        ),
        "score_artifact_count": len(score_artifacts),
        "historical_metric_comparison_count": len(comparison_rows),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
