"""Frozen five-model registry and factory."""

from formal_gcn_v1 import FormalGCN
from formal_graphsage_v1 import FormalGraphSAGE
from formal_heterosage_v1 import FormalHeteroSAGE
from formal_rgcn_v1 import FormalRGCN
from formal_tcmrgat_v1 import FormalTCMRGAT


FORMAL_MODELS = {
    "TCMRGAT": FormalTCMRGAT,
    "HeteroSAGE": FormalHeteroSAGE,
    "GraphSAGE": FormalGraphSAGE,
    "RGCN": FormalRGCN,
    "GCN": FormalGCN,
}


def build_model(model_name, feature_builder, config, relation_count):
    if model_name not in FORMAL_MODELS:
        raise KeyError(model_name)
    kwargs = dict(
        feature_builder=feature_builder,
        hidden_dim=int(config["hidden_dim"]),
        relation_count=relation_count,
        layers=int(config["layers"]),
        dropout=float(config["dropout"]),
    )
    if model_name == "TCMRGAT":
        kwargs["heads"] = 4
    if model_name == "RGCN":
        kwargs["num_bases"] = min(4, relation_count)
    return FORMAL_MODELS[model_name](**kwargs)
