#!/usr/bin/env python3
"""Score a third-party or archived score matrix against the public fixed test set.

The score matrix must be an NPZ created with the open-score format: `scores`,
`herb_ids`, and `target_ids`.  Axes must already match the fixed public graph;
this utility never silently reorders them.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

from formal_test_score_runner_v1 import import_frozen_d1


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def resolve_path(package_root: Path, value: Path) -> Path:
    return value.resolve() if value.is_absolute() else (package_root / value).resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--score-matrix", type=Path, required=True)
    parser.add_argument("--labels", type=Path, default=Path("data/labels/test_positive_pairs_v1.csv"))
    parser.add_argument("--candidate-targets", type=Path, default=Path("data/graph/candidate_target_universe_v1.csv"))
    parser.add_argument("--test-herbs", type=Path, default=Path("data/graph/test_query_herb_nodes_v1.csv"))
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    package_root = args.package_root.resolve()
    score_path = resolve_path(package_root, args.score_matrix)
    label_path = resolve_path(package_root, args.labels)
    candidate_path = resolve_path(package_root, args.candidate_targets)
    herb_path = resolve_path(package_root, args.test_herbs)
    label_rows = read_csv(label_path)
    pairs = [(row["herb_id"], row["target_id"]) for row in label_rows]
    candidate_rows = sorted(read_csv(candidate_path), key=lambda row: int(row["candidate_order"]))
    expected_targets = [row["target_id"] for row in candidate_rows]
    expected_herbs = sorted(row["herb_id"] for row in read_csv(herb_path))
    with np.load(score_path, allow_pickle=False) as payload:
        scores = np.asarray(payload["scores"], dtype=np.float64)
        herb_ids = [str(value) for value in payload["herb_ids"].tolist()]
        target_ids = [str(value) for value in payload["target_ids"].tolist()]
        metadata = str(payload["metadata_json"].item()) if "metadata_json" in payload else ""
    if herb_ids != expected_herbs or target_ids != expected_targets:
        raise RuntimeError("SCORE_MATRIX_AXIS_MISMATCH")
    if scores.shape != (len(expected_herbs), len(expected_targets)):
        raise RuntimeError("SCORE_MATRIX_SHAPE_MISMATCH")
    frozen_d1 = import_frozen_d1(package_root / "src" / "frozen_d1")
    scores_by_herb = {herb: scores[index].tolist() for index, herb in enumerate(herb_ids)}
    summary, per_herb = frozen_d1["evaluate"](scores_by_herb, target_ids, pairs)
    result = {
        "score_matrix": score_path.name,
        "score_metadata_json": metadata,
        "test_herb_count": len(herb_ids),
        "candidate_target_count": len(target_ids),
        "recorded_positive_pair_count": len(pairs),
        "summary": summary,
        "per_herb_metrics": per_herb,
    }
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        output_path = resolve_path(package_root, args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise
