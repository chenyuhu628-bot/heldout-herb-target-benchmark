"""Frozen positive-unlabeled validation metric contract."""

from __future__ import annotations

from collections import defaultdict

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


KS = (10, 20, 50)


def _validate(scores_by_herb, target_ids, positives):
    if len(target_ids) != len(set(target_ids)):
        raise ValueError("DUPLICATE_TARGET_ID")
    grouped = defaultdict(set)
    for herb, target in positives:
        grouped[herb].add(target)
    if set(scores_by_herb) != set(grouped):
        raise ValueError("HERB_COVERAGE_MISMATCH")
    for herb, scores in scores_by_herb.items():
        values = np.asarray(scores, dtype=float)
        if len(values) != len(target_ids):
            raise ValueError("CANDIDATE_LENGTH_MISMATCH")
        if not np.isfinite(values).all():
            raise ValueError("NONFINITE_SCORE")
        labels = np.asarray([int(t in grouped[herb]) for t in target_ids], dtype=int)
        if labels.sum() == 0:
            raise ValueError("HERB_WITHOUT_POSITIVE")
        if labels.sum() == len(labels):
            raise ValueError("ALL_POSITIVE_VECTOR")
    return grouped


def evaluate_formal_validation(scores_by_herb, target_ids, validation_positives):
    grouped = _validate(scores_by_herb, target_ids, validation_positives)
    target_array = np.asarray(target_ids, dtype=str)
    per_herb = []
    micro_scores, micro_labels = [], []
    for herb in sorted(grouped):
        scores = np.asarray(scores_by_herb[herb], dtype=float)
        labels = np.asarray([int(t in grouped[herb]) for t in target_ids], dtype=int)
        order = np.lexsort((target_array, -scores))
        ranked = labels[order]
        positive_count = int(labels.sum())
        row = {
            "herb_id": herb,
            "aupr": float(average_precision_score(labels, scores)),
            "auroc": float(roc_auc_score(labels, scores)),
        }
        positive_ranks = np.where(ranked == 1)[0] + 1
        row["mrr_first_positive"] = float(1.0 / positive_ranks.min())
        for k in KS:
            top = ranked[: min(k, len(ranked))]
            row[f"recall_at_{k}"] = float(top.sum() / positive_count)
            discounts = 1.0 / np.log2(np.arange(2, len(top) + 2))
            dcg = float(np.sum(top * discounts))
            ideal_len = min(positive_count, len(top))
            idcg = float(np.sum(discounts[:ideal_len]))
            row[f"ndcg_at_{k}"] = dcg / idcg if idcg else 0.0
        per_herb.append(row)
        micro_scores.extend(scores.tolist())
        micro_labels.extend(labels.tolist())
    summary = {
        "macro_aupr": float(np.mean([r["aupr"] for r in per_herb])),
        "macro_auroc": float(np.mean([r["auroc"] for r in per_herb])),
        "micro_aupr": float(average_precision_score(micro_labels, micro_scores)),
        "micro_auroc": float(roc_auc_score(micro_labels, micro_scores)),
        "mrr_first_positive": float(np.mean([r["mrr_first_positive"] for r in per_herb])),
        "evaluated_herb_count": len(per_herb),
        "candidate_target_count": len(target_ids),
    }
    for k in KS:
        summary[f"recall_at_{k}"] = float(np.mean([r[f"recall_at_{k}"] for r in per_herb]))
        summary[f"ndcg_at_{k}"] = float(np.mean([r[f"ndcg_at_{k}"] for r in per_herb]))
    return summary, per_herb


PRIMARY_METRIC = "macro_aupr"
TIE_BREAK_ORDER = ["macro_auroc", "recall_at_50", "lower_parameter_count", "lexicographically_smaller_config_id"]
