# Archived frozen score matrices

This directory contains 25 complete score matrices, one for each fixed best checkpoint listed in artifacts/checkpoints/checkpoint_manifest_v1.csv.

Each NPZ archive contains:

    scores         float64 array with shape (67, 2309)
    herb_ids       exact public test-herb axis
    target_ids     exact public candidate-target axis
    metadata_json  checkpoint and score-semantics metadata

Scores are raw decoder logits, not calibrated probabilities. The axis order is binding. Use src/evaluation/evaluate_score_matrix_v1.py to calculate metrics without silently changing the axes.

The machine-readable inventory and SHA-256 digests are in results/metrics/open_frozen_score_export_manifest_v1.json and CHECKSUMS_SHA256.txt.
