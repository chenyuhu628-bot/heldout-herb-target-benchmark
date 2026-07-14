"""Frozen-checkpoint, all-target scoring for the one-time formal test."""

from __future__ import annotations

import csv
import importlib
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import torch


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def import_frozen_d1(d1: Path) -> dict[str, Any]:
    sys.path.insert(0, str(d1))
    feature = importlib.import_module("formal_feature_builder_v1")
    models = importlib.import_module("formal_model_registry_v1")
    metrics = importlib.import_module("formal_metric_contract_v1")
    return {
        "FeatureBuilder": feature.FormalFeatureBuilder,
        "build_model": models.build_model,
        "evaluate": metrics.evaluate_formal_validation,
    }


def prepare_scoring_data(c3: Path, device: torch.device) -> dict[str, Any]:
    nodes = sorted(read_csv(c3 / "training_graph_node_index_v1.csv"), key=lambda row: int(row["node_index"]))
    node_to_index = {row["node_id"]: int(row["node_index"]) for row in nodes}
    compounds = [int(row["node_index"]) for row in nodes if row["node_type"] == "compound"]
    targets = [row for row in nodes if row["node_type"] == "target"]
    relation_rows = sorted(read_csv(c3 / "training_graph_relation_index_v1.csv"), key=lambda row: int(row["relation_index"]))
    relation_map = {row["relation_name"]: int(row["relation_index"]) for row in relation_rows}
    edge_rows = read_csv(c3 / "training_graph_nonlabel_edges_v1.csv")
    edge_index = torch.tensor(
        [
            [node_to_index[row["source_node_id"]] for row in edge_rows],
            [node_to_index[row["target_node_id"]] for row in edge_rows],
        ],
        dtype=torch.long,
        device=device,
    )
    relation_ids = torch.tensor(
        [relation_map[row["relation_name"]] for row in edge_rows],
        dtype=torch.long,
        device=device,
    )
    train_context: dict[int, list[int]] = defaultdict(list)
    for row in edge_rows:
        if row["relation_name"] == "herb_contains_compound":
            train_context[node_to_index[row["source_node_id"]]].append(node_to_index[row["target_node_id"]])
    query_context: dict[str, list[int]] = defaultdict(list)
    for row in read_csv(c3 / "test_query_herb_compound_edges_v1.csv"):
        query_context[row["herb_id"]].append(node_to_index[row["compound_id"]])
    query_nodes = [row["herb_id"] for row in read_csv(c3 / "test_query_herb_nodes_v1.csv")]
    if set(query_context) != set(query_nodes) or len(query_nodes) != 67:
        raise RuntimeError("TEST_QUERY_CONTEXT_COVERAGE_FAILURE")
    return {
        "nodes": nodes,
        "compounds": compounds,
        "target_indices": [int(row["node_index"]) for row in targets],
        "target_ids": [row["node_id"] for row in targets],
        "relation_map": relation_map,
        "edge_index": edge_index,
        "relation_ids": relation_ids,
        "train_context": dict(train_context),
        "query_context": dict(query_context),
    }


def infer_eval_config(model_name: str, state: dict[str, torch.Tensor]) -> dict[str, str]:
    hidden = int(state["feature_builder.compound_embedding.weight"].shape[1])
    prefix = "relation_layers." if model_name in {"TCMRGAT", "HeteroSAGE"} else "layers."
    indices = {
        int(key.split(".")[1])
        for key in state
        if key.startswith(prefix) and len(key.split(".")) > 2 and key.split(".")[1].isdigit()
    }
    return {"hidden_dim": str(hidden), "layers": str(max(indices) + 1), "dropout": "0.0"}


def build_model_from_state(
    frozen: dict[str, Any],
    data: dict[str, Any],
    model_name: str,
    state: dict[str, torch.Tensor],
    device: torch.device,
) -> torch.nn.Module:
    config = infer_eval_config(model_name, state)
    builder = frozen["FeatureBuilder"](
        num_nodes=len(data["nodes"]),
        compound_global_indices=data["compounds"],
        target_global_indices=data["target_indices"],
        herb_context=data["train_context"],
        hidden_dim=int(config["hidden_dim"]),
    )
    model = frozen["build_model"](model_name, builder, config, len(data["relation_map"])).to(device)
    model.load_state_dict(state, strict=True)
    model.eval()
    return model


@torch.no_grad()
def score_all_test_targets(
    model: torch.nn.Module,
    data: dict[str, Any],
    query_batch_size: int = 16,
) -> tuple[list[str], np.ndarray]:
    device = data["edge_index"].device
    base_features = model.feature_builder.build_training_features()
    base_node_count = base_features.shape[0]
    base_targets = torch.tensor(data["target_indices"], dtype=torch.long, device=device)
    herb_ids = sorted(data["query_context"])
    blocks = []
    for start in range(0, len(herb_ids), query_batch_size):
        herbs = herb_ids[start:start + query_batch_size]
        features, edges, relations, queries, target_blocks = [], [], [], [], []
        for batch_index, herb_id in enumerate(herbs):
            offset = batch_index * (base_node_count + 1)
            compounds = torch.tensor(data["query_context"][herb_id], dtype=torch.long, device=device)
            query_feature = model.feature_builder.encode_compound_context(data["query_context"][herb_id])
            features.append(torch.cat([base_features, query_feature.view(1, -1)], dim=0))
            query_index = offset + base_node_count
            queries.append(query_index)
            query_nodes = torch.full((len(compounds),), query_index, dtype=torch.long, device=device)
            edges.extend(
                [
                    data["edge_index"] + offset,
                    torch.stack([query_nodes, compounds + offset]),
                    torch.stack([compounds + offset, query_nodes]),
                ]
            )
            relations.extend(
                [
                    data["relation_ids"],
                    torch.full((len(compounds),), data["relation_map"]["herb_contains_compound"], dtype=torch.long, device=device),
                    torch.full((len(compounds),), data["relation_map"]["compound_in_herb"], dtype=torch.long, device=device),
                ]
            )
            target_blocks.append(base_targets + offset)
        z = model._encode(torch.cat(features), torch.cat(edges, dim=1), torch.cat(relations))
        logits = model.score_pairs(
            z,
            torch.repeat_interleave(
                torch.tensor(queries, dtype=torch.long, device=device),
                len(data["target_ids"]),
            ),
            torch.cat(target_blocks),
        ).view(len(herbs), len(data["target_ids"]))
        blocks.append(logits.detach().cpu().double().numpy())
    return herb_ids, np.vstack(blocks)


def evaluate_scores(
    frozen: dict[str, Any],
    herb_ids: list[str],
    scores: np.ndarray,
    target_ids: list[str],
    positive_pairs: list[tuple[str, str]],
) -> tuple[dict[str, float], list[dict[str, float]]]:
    scores_by_herb = {herb: scores[index].tolist() for index, herb in enumerate(herb_ids)}
    return frozen["evaluate"](scores_by_herb, target_ids, positive_pairs)
