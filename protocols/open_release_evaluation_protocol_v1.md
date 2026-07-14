# Open fixed-test evaluation protocol, v1

## Purpose and status

This protocol governs the public v1.2 reproducibility release. It is intentionally separate from the historical sealed-test protocol. The historical sealed evaluation was completed before public disclosure; this package opens the fixed test assets so that readers can inspect rankings and independently calculate the archived metrics.

The public fixed test is an evaluation reference set, not an ongoing blinded generalization test. Any method developed after observing the labels, scores, rankings, or reported metrics must be described as evaluated on a public fixed test and not as a prospective held-out evaluation.

## Fixed public assets

The package fixes the following assets:

- 67 test herbs in data/labels/test_positive_herbs_v1.csv;
- 8,632 recorded-positive test pairs in data/labels/test_positive_pairs_v1.csv;
- 2,309 candidate targets in data/graph/candidate_target_universe_v1.csv;
- frozen training graph and test query context in data/graph;
- 25 selected best checkpoints in artifacts/checkpoints/checkpoint_manifest_v1.csv;
- 25 complete raw decoder-logit matrices in artifacts/scores;
- metric implementation in src/frozen_d1/formal_metric_contract_v1.py.

The axes in every packaged score NPZ are part of the artifact. The evaluator requires the provided herb_ids and target_ids to exactly equal the archived axes; it does not silently sort, map, intersect, or otherwise repair them.

## Permitted operations

Readers may:

- recompute the reported metrics from an archived score matrix;
- inspect complete rankings and per-herb results;
- rerun frozen checkpoint inference using the archived graph, labels, code, and checkpoint manifest;
- evaluate an external score matrix that follows the exact public axes and records its provenance.

## Prohibited uses for claims of held-out performance

The following operations invalidate a claim that a result is a blinded held-out evaluation on this test:

- selecting a model family, feature set, hyperparameter, seed, epoch, threshold, or checkpoint using these public labels or metrics;
- tuning a method after observing test rankings, labels, score matrices, or aggregate outcomes;
- changing the candidate target universe, graph, labels, metric definition, or axis order and reporting the result as the archived benchmark;
- using this test as the only assessment of a newly developed model.

## Frozen-checkpoint reproduction

The command src/evaluation/export_frozen_test_scores_v1.py reconstructs scores from the 25 archived checkpoints. Before scoring, it verifies fixed checkpoint identities, file sizes, SHA-256 digests, checkpoint metadata, frozen D1 implementation hashes, label counts, candidate targets, and test-query axes. It then compares all eleven metrics for each checkpoint with the historical reference metrics at absolute and relative tolerance 1e-6.

The command does not perform training, validation, tuning, model selection, checkpoint selection, or post-test adaptation. A successful run is evidence that the released frozen artifacts reproduce the historical calculation. It is not a new sealed-test result.

## Independent score-matrix evaluation

The command src/evaluation/evaluate_score_matrix_v1.py accepts a third-party NPZ file only when it contains a complete score matrix with the exact public herb and target axes. It evaluates recorded-positive label recovery using the archived metric contract. Users should report the origin of their score matrix, whether the public labels were visible during development, and all adaptation or selection steps.

## Interpretation

The positive labels are observed records, not exhaustive ground truth. Metrics should be interpreted as the ability to rank archived recorded positives within this fixed candidate universe. The protocol does not establish similarity-disjoint, provenance-complete, prospective, or clinical generalization.
