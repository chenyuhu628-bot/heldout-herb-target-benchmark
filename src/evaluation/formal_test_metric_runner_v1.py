"""Aggregate and paired descriptive statistics for formal test metrics."""

from __future__ import annotations

from itertools import combinations
from typing import Any

import numpy as np


MODELS = ["TCMRGAT", "HeteroSAGE", "GraphSAGE", "RGCN", "GCN"]
METRICS = [
    "macro_aupr", "macro_auroc", "micro_aupr", "micro_auroc",
    "recall_at_10", "recall_at_20", "recall_at_50",
    "ndcg_at_10", "ndcg_at_20", "ndcg_at_50", "mrr_first_positive",
]


def aggregate_by_model(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for model in MODELS:
        group = [row for row in rows if row["model"] == model]
        item: dict[str, Any] = {
            "model": model, "config_id": group[0]["config_id"], "seed_count": len(group),
            "primary_metric": "macro herb-level AUPR", "one_time_test": True,
            "final_test_result": True,
        }
        for metric in METRICS:
            values = np.asarray([float(row[metric]) for row in group])
            item[f"mean_{metric}"] = float(values.mean())
            item[f"std_{metric}"] = float(values.std(ddof=1))
        output.append(item)
    return output


def uncertainty(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for model in MODELS:
        group = [row for row in rows if row["model"] == model]
        for metric in METRICS:
            values = np.asarray([float(row[metric]) for row in group])
            output.append({
                "model": model, "metric": metric, "seed_count": len(values),
                "mean": float(values.mean()), "std": float(values.std(ddof=1)),
                "sem": float(values.std(ddof=1) / np.sqrt(len(values))),
                "percentile_2_5": float(np.percentile(values, 2.5)),
                "percentile_97_5": float(np.percentile(values, 97.5)),
                "interval_method": "descriptive seed-level percentile interval; n=5; not strong inferential CI",
                "final_test_result": True,
            })
    return output


def pairwise_seed_deltas(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    indexed = {(row["model"], row["seed_name"]): row for row in rows}
    seeds = sorted({row["seed_name"] for row in rows})
    output = []
    for model_a, model_b in combinations(MODELS, 2):
        for seed in seeds:
            a, b = indexed[(model_a, seed)], indexed[(model_b, seed)]
            for metric in METRICS:
                output.append({
                    "model_a": model_a, "model_b": model_b, "seed_name": seed,
                    "metric": metric, "value_a": a[metric], "value_b": b[metric],
                    "delta_a_minus_b": float(a[metric]) - float(b[metric]),
                    "paired_by_seed": True, "final_test_result": True,
                })
    return output


def paired_comparisons(delta_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    pairs = sorted({(row["model_a"], row["model_b"]) for row in delta_rows})
    for model_a, model_b in pairs:
        for metric in METRICS:
            group = [
                float(row["delta_a_minus_b"]) for row in delta_rows
                if row["model_a"] == model_a and row["model_b"] == model_b and row["metric"] == metric
            ]
            values = np.asarray(group)
            mean = float(values.mean())
            sign = np.sign(mean)
            consistency = float(np.mean(np.sign(values) == sign)) if sign else float(np.mean(values == 0))
            output.append({
                "model_a": model_a, "model_b": model_b, "metric": metric,
                "paired_seed_count": len(values), "paired_mean_delta_a_minus_b": mean,
                "paired_std_delta": float(values.std(ddof=1)), "paired_median_delta": float(np.median(values)),
                "direction_consistency": consistency,
                "p_value": "NA", "p_value_policy": "not computed; n=5 descriptive comparison",
                "comparison_scope": "exploratory_descriptive_paired_frozen_seeds",
                "final_test_result": True,
            })
    return output
