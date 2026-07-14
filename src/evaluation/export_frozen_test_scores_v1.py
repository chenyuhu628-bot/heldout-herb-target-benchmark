#!/usr/bin/env python3
"""Export open fixed-test scores from the 25 frozen final checkpoints.

This is a public reproducibility entry point.  It does not train, tune, select,
or modify a model.  It re-scores the public fixed test set with the archived
best checkpoints and checks every reproduced metric against the historical
one-time sealed-evaluation reference.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import torch

from formal_test_metric_runner_v1 import METRICS
from formal_test_score_runner_v1 import (
    build_model_from_state,
    evaluate_scores,
    import_frozen_d1,
    prepare_scoring_data,
    score_all_test_targets,
)


EXPECTED_MODELS = {"TCMRGAT", "HeteroSAGE", "GraphSAGE", "RGCN", "GCN"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_path(package_root: Path, value: Path) -> Path:
    return value.resolve() if value.is_absolute() else (package_root / value).resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--graph-dir", type=Path, default=Path("data/graph"))
    parser.add_argument("--labels", type=Path, default=Path("data/labels/test_positive_pairs_v1.csv"))
    parser.add_argument("--checkpoint-manifest", type=Path, default=Path("artifacts/checkpoints/checkpoint_manifest_v1.csv"))
    parser.add_argument("--reference-metrics", type=Path, default=Path("results/reference/historical_test_metrics_by_checkpoint_v1.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/scores"))
    parser.add_argument("--metrics-dir", type=Path, default=Path("results/metrics"))
    parser.add_argument("--device", default="auto", help="auto, cpu, cuda, or a valid torch device string")
    parser.add_argument("--query-batch-size", type=int, default=16)
    parser.add_argument("--verify-atol", type=float, default=1e-6)
    parser.add_argument("--verify-rtol", type=float, default=1e-6)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def select_device(value: str) -> torch.device:
    if value == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device(value)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA_REQUESTED_BUT_UNAVAILABLE")
    return device


def load_public_labels(path: Path) -> list[tuple[str, str]]:
    rows = read_csv(path)
    if not rows or set(rows[0]) != {"herb_id", "target_id"}:
        raise RuntimeError("TEST_LABEL_SCHEMA_MISMATCH")
    pairs = [(row["herb_id"], row["target_id"]) for row in rows]
    if len(pairs) != 8632 or len(set(pairs)) != 8632:
        raise RuntimeError(f"TEST_LABEL_PAIR_COUNT_MISMATCH:{len(pairs)}")
    if len({herb for herb, _ in pairs}) != 67:
        raise RuntimeError("TEST_LABEL_HERB_COUNT_MISMATCH")
    return pairs


def load_candidate_targets(path: Path) -> list[str]:
    rows = read_csv(path)
    required = {"target_id", "node_index", "candidate_order"}
    if not rows or set(rows[0]) != required:
        raise RuntimeError("CANDIDATE_TARGET_SCHEMA_MISMATCH")
    rows = sorted(rows, key=lambda row: int(row["candidate_order"]))
    expected_order = list(range(len(rows)))
    observed_order = [int(row["candidate_order"]) for row in rows]
    if observed_order != expected_order or len(rows) != 2309:
        raise RuntimeError("CANDIDATE_TARGET_ORDER_OR_COUNT_MISMATCH")
    return [row["target_id"] for row in rows]


def load_checkpoint_manifest(path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    required = {
        "model", "config_id", "seed_name", "run_id", "checkpoint_type", "relative_path", "size_bytes",
        "sha256", "formal_protocol_version", "config_hash", "run_seed",
    }
    if len(rows) != 25 or not rows or set(rows[0]) != required:
        raise RuntimeError("CHECKPOINT_MANIFEST_SCHEMA_OR_COUNT_MISMATCH")
    run_ids = {row["run_id"] for row in rows}
    models = {row["model"] for row in rows}
    if len(run_ids) != 25 or models != EXPECTED_MODELS or any(row["checkpoint_type"] != "best" for row in rows):
        raise RuntimeError("CHECKPOINT_MANIFEST_INVARIANT_FAILURE")
    by_model = Counter(row["model"] for row in rows)
    if any(by_model[model] != 5 for model in EXPECTED_MODELS):
        raise RuntimeError("CHECKPOINT_MANIFEST_SEED_COUNT_FAILURE")
    return sorted(rows, key=lambda row: (row["model"], row["seed_name"]))


def load_reference_metrics(path: Path) -> dict[tuple[str, str, str], dict[str, str]]:
    rows = read_csv(path)
    if len(rows) != 25:
        raise RuntimeError("HISTORICAL_REFERENCE_METRIC_COUNT_MISMATCH")
    indexed = {(row["model"], row["config_id"], row["seed_name"]): row for row in rows}
    if len(indexed) != 25 or any(metric not in next(iter(indexed.values())) for metric in METRICS):
        raise RuntimeError("HISTORICAL_REFERENCE_METRIC_SCHEMA_MISMATCH")
    return indexed


def verify_frozen_code_hashes(frozen_d1_dir: Path, metadata: dict[str, Any]) -> None:
    input_hashes = metadata.get("input_hashes", {})
    for module in sorted(frozen_d1_dir.glob("*.py")):
        expected = [value for key, value in input_hashes.items() if Path(key).name == module.name]
        if len(expected) != 1:
            raise RuntimeError(f"FROZEN_CODE_HASH_NOT_UNAMBIGUOUS:{module.name}")
        if sha256_file(module) != expected[0]:
            raise RuntimeError(f"FROZEN_CODE_HASH_MISMATCH:{module.name}")


def verify_checkpoint(
    path: Path,
    row: dict[str, str],
    device: torch.device,
    frozen_d1_dir: Path,
) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(f"MISSING_CHECKPOINT:{path}")
    if path.stat().st_size != int(row["size_bytes"]):
        raise RuntimeError(f"CHECKPOINT_SIZE_MISMATCH:{row['run_id']}")
    observed_hash = sha256_file(path)
    if observed_hash != row["sha256"]:
        raise RuntimeError(f"CHECKPOINT_HASH_MISMATCH:{row['run_id']}")
    payload = torch.load(path, map_location=device, weights_only=True)
    metadata = payload.get("metadata", {})
    expected = {
        "model_name": row["model"],
        "config_id": row["config_id"],
        "seed_name": row["seed_name"],
        "run_id": row["run_id"],
        "config_hash": row["config_hash"],
        "formal_protocol_version": row["formal_protocol_version"],
    }
    for key, value in expected.items():
        if metadata.get(key) != value:
            raise RuntimeError(f"CHECKPOINT_METADATA_MISMATCH:{row['run_id']}:{key}")
    verify_frozen_code_hashes(frozen_d1_dir, metadata)
    return payload


def refuse_overwrite(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise RuntimeError(f"REFUSING_TO_OVERWRITE:{path}")


def save_score_matrix(
    path: Path,
    scores: np.ndarray,
    herb_ids: list[str],
    target_ids: list[str],
    metadata: dict[str, Any],
    overwrite: bool,
) -> str:
    refuse_overwrite(path, overwrite)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        scores=np.asarray(scores, dtype=np.float64),
        herb_ids=np.asarray(herb_ids, dtype=str),
        target_ids=np.asarray(target_ids, dtype=str),
        metadata_json=np.asarray(json.dumps(metadata, sort_keys=True), dtype=str),
    )
    return sha256_file(path)


def tolerance_pass(observed: float, expected: float, atol: float, rtol: float) -> bool:
    return abs(observed - expected) <= atol + rtol * abs(expected)


def main() -> None:
    args = parse_args()
    package_root = args.package_root.resolve()
    graph_dir = resolve_path(package_root, args.graph_dir)
    labels_path = resolve_path(package_root, args.labels)
    checkpoint_manifest_path = resolve_path(package_root, args.checkpoint_manifest)
    reference_metrics_path = resolve_path(package_root, args.reference_metrics)
    output_dir = resolve_path(package_root, args.output_dir)
    metrics_dir = resolve_path(package_root, args.metrics_dir)
    device = select_device(args.device)

    public_pairs = load_public_labels(labels_path)
    candidate_targets = load_candidate_targets(graph_dir / "candidate_target_universe_v1.csv")
    checkpoint_rows = load_checkpoint_manifest(checkpoint_manifest_path)
    historical_reference = load_reference_metrics(reference_metrics_path)
    frozen_d1 = import_frozen_d1(package_root / "src" / "frozen_d1")
    data = prepare_scoring_data(graph_dir, device)

    if data["target_ids"] != candidate_targets:
        raise RuntimeError("CANDIDATE_TARGET_AXIS_MISMATCH")
    if len(data["target_ids"]) != 2309 or len(data["query_context"]) != 67:
        raise RuntimeError("GRAPH_SCORING_UNIVERSE_MISMATCH")
    label_herbs = {herb for herb, _ in public_pairs}
    label_targets = {target for _, target in public_pairs}
    if label_herbs != set(data["query_context"]) or not label_targets <= set(data["target_ids"]):
        raise RuntimeError("PUBLIC_LABEL_AND_GRAPH_UNIVERSE_MISMATCH")

    metric_rows: list[dict[str, Any]] = []
    per_herb_rows: list[dict[str, Any]] = []
    comparison_rows: list[dict[str, Any]] = []
    score_artifacts: list[dict[str, Any]] = []
    all_metrics_match = True

    for row in checkpoint_rows:
        checkpoint_path = package_root / row["relative_path"]
        payload = verify_checkpoint(checkpoint_path, row, device, package_root / "src" / "frozen_d1")
        model = build_model_from_state(frozen_d1, data, row["model"], payload["state_dict"], device)
        herb_ids, scores = score_all_test_targets(model, data, query_batch_size=args.query_batch_size)
        if herb_ids != sorted(label_herbs) or scores.shape != (67, 2309):
            raise RuntimeError(f"SCORE_MATRIX_AXIS_MISMATCH:{row['run_id']}")
        summary, per_herb = evaluate_scores(frozen_d1, herb_ids, scores, data["target_ids"], public_pairs)
        reference = historical_reference[(row["model"], row["config_id"], row["seed_name"])]
        metadata = {
            "format_version": "open_frozen_score_matrix_v1",
            "score_semantics": "raw_decoder_logits; not calibrated probabilities",
            "model": row["model"],
            "config_id": row["config_id"],
            "seed_name": row["seed_name"],
            "run_id": row["run_id"],
            "checkpoint_sha256": row["sha256"],
            "candidate_target_count": 2309,
            "test_herb_count": 67,
            "recorded_positive_pair_count": 8632,
            "public_fixed_test": True,
            "post_release_export_only": True,
            "model_selection_performed": False,
        }
        score_path = output_dir / f"{row['run_id']}_scores_v1.npz"
        score_hash = save_score_matrix(score_path, scores, herb_ids, data["target_ids"], metadata, args.overwrite)
        score_artifacts.append(
            {
                "run_id": row["run_id"],
                "relative_path": score_path.relative_to(package_root).as_posix(),
                "sha256": score_hash,
                "shape": [67, 2309],
                "score_semantics": metadata["score_semantics"],
            }
        )
        metric_row = {
            "model": row["model"],
            "config_id": row["config_id"],
            "seed_name": row["seed_name"],
            "run_id": row["run_id"],
            "relative_checkpoint_path": row["relative_path"],
            "checkpoint_sha256": row["sha256"],
            "test_herb_count": 67,
            "target_count": 2309,
            "test_positive_pair_count": 8632,
            **{metric: summary[metric] for metric in METRICS},
            "public_fixed_test": True,
            "post_release_export_only": True,
            "model_selection_performed": False,
        }
        metric_rows.append(metric_row)
        positive_counts = Counter(herb for herb, _ in public_pairs)
        for item in per_herb:
            per_herb_rows.append(
                {
                    "model": row["model"],
                    "config_id": row["config_id"],
                    "seed_name": row["seed_name"],
                    "run_id": row["run_id"],
                    "test_herb_id": item["herb_id"],
                    "recorded_positive_count": positive_counts[item["herb_id"]],
                    "target_count": 2309,
                    "herb_aupr": item["aupr"],
                    "herb_auroc": item["auroc"],
                    "recall_at_10": item["recall_at_10"],
                    "recall_at_20": item["recall_at_20"],
                    "recall_at_50": item["recall_at_50"],
                    "ndcg_at_10": item["ndcg_at_10"],
                    "ndcg_at_20": item["ndcg_at_20"],
                    "ndcg_at_50": item["ndcg_at_50"],
                    "mrr_first_positive": item["mrr_first_positive"],
                    "public_fixed_test": True,
                    "post_release_export_only": True,
                }
            )
        for metric in METRICS:
            observed = float(summary[metric])
            expected = float(reference[metric])
            passed = tolerance_pass(observed, expected, args.verify_atol, args.verify_rtol)
            all_metrics_match &= passed
            comparison_rows.append(
                {
                    "model": row["model"],
                    "config_id": row["config_id"],
                    "seed_name": row["seed_name"],
                    "run_id": row["run_id"],
                    "metric": metric,
                    "historical_reference": expected,
                    "reproduced_public_export": observed,
                    "absolute_difference": abs(observed - expected),
                    "within_tolerance": passed,
                    "atol": args.verify_atol,
                    "rtol": args.verify_rtol,
                }
            )
        del model, payload, scores
        if device.type == "cuda":
            torch.cuda.empty_cache()

    metric_fields = [
        "model", "config_id", "seed_name", "run_id", "relative_checkpoint_path", "checkpoint_sha256",
        "test_herb_count", "target_count", "test_positive_pair_count", *METRICS,
        "public_fixed_test", "post_release_export_only", "model_selection_performed",
    ]
    per_herb_fields = [
        "model", "config_id", "seed_name", "run_id", "test_herb_id", "recorded_positive_count", "target_count",
        "herb_aupr", "herb_auroc", "recall_at_10", "recall_at_20", "recall_at_50", "ndcg_at_10",
        "ndcg_at_20", "ndcg_at_50", "mrr_first_positive", "public_fixed_test", "post_release_export_only",
    ]
    comparison_fields = [
        "model", "config_id", "seed_name", "run_id", "metric", "historical_reference",
        "reproduced_public_export", "absolute_difference", "within_tolerance", "atol", "rtol",
    ]
    write_csv(metrics_dir / "reproduced_test_metrics_by_checkpoint_v1.csv", metric_rows, metric_fields)
    write_csv(metrics_dir / "reproduced_test_per_herb_metrics_v1.csv", per_herb_rows, per_herb_fields)
    write_csv(metrics_dir / "historical_metric_reproduction_comparison_v1.csv", comparison_rows, comparison_fields)
    export_manifest = {
        "version": "open_frozen_score_export_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "device": str(device),
        "score_semantics": "raw_decoder_logits; not calibrated probabilities",
        "test_set_status": "public fixed test set; historical evaluation was sealed before disclosure",
        "post_release_export_only": True,
        "retraining_performed": False,
        "tuning_performed": False,
        "model_reselection_performed": False,
        "test_herb_count": 67,
        "candidate_target_count": 2309,
        "recorded_positive_pair_count": 8632,
        "checkpoint_count": len(checkpoint_rows),
        "score_artifacts": score_artifacts,
        "reproduced_metric_count": len(comparison_rows),
        "historical_metric_match": all_metrics_match,
        "verification_atol": args.verify_atol,
        "verification_rtol": args.verify_rtol,
    }
    write_json(metrics_dir / "open_frozen_score_export_manifest_v1.json", export_manifest)
    print(json.dumps(export_manifest, indent=2, sort_keys=True))
    if not all_metrics_match:
        raise RuntimeError("HISTORICAL_METRIC_REPRODUCTION_FAILURE")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise
