# Open reproducibility release audit, v1

## Release state

This audit applies to the v1.2 open reproducibility release. It supersedes earlier access-scope claims that described the fixed test labels, score matrices, or selected checkpoints as non-public. Historical sealed-evaluation records are retained only as provenance evidence.

## Fixed public test inventory

| Asset | Expected value | Public package location |
| --- | ---: | --- |
| Test herbs | 67 | data/labels/test_positive_herbs_v1.csv |
| Recorded-positive test pairs | 8,632 | data/labels/test_positive_pairs_v1.csv |
| Candidate targets | 2,309 | data/graph/candidate_target_universe_v1.csv |
| Selected final checkpoints | 25 | artifacts/checkpoints/checkpoint_manifest_v1.csv |
| Models | 5 | GCN, GraphSAGE, HeteroSAGE, RGCN, TCMRGAT |
| Final seeds per model | 5 | FINAL_01 through FINAL_05 |
| Complete score matrices | 25 | artifacts/scores |
| Score shape per matrix | 67 by 2,309 | self-described NPZ arrays |
| Historical metric comparisons | 275 | 25 checkpoints multiplied by 11 metrics |

## Integrity results

The current score-export record in results/metrics/open_frozen_score_export_manifest_v1.json reports:

- checkpoint_count: 25;
- candidate_target_count: 2,309;
- recorded_positive_pair_count: 8,632;
- historical_metric_match: true;
- reproduced_metric_count: 275;
- retraining_performed: false;
- model_reselection_performed: false;
- post_release_export_only: true.

Each score matrix is bound to a named checkpoint through a SHA-256-recorded manifest. The exporter validates the original frozen D1 implementation hashes recorded in checkpoint metadata before inference. The checker does not accept a directory scan as a substitute for the 25-row fixed checkpoint manifest.

Before public release, machine-local path strings in copied checkpoint metadata were replaced with portable identifiers. The release serializations therefore have new SHA-256 values, while a deterministic state_dict content fingerprint was checked before and after each metadata-only rewrite. The source and release hashes are retained in data/provenance/checkpoint_metadata_path_sanitization_v1.json.

## Public access and interpretation boundary

No approval or application is required to obtain the fixed test labels, full scores, or selected checkpoints in this package. Because these assets are now public, this test set cannot be represented as a continuing hidden test for any post-release method-development decision.

The historical sealed metrics may still be reported as historical results if the timing and information boundary are stated accurately. Any new analysis using these public labels must be reported as evaluation on the public fixed test set.

## External-source boundary

The package includes a frozen derived graph and provenance summaries, not a complete mirror of third-party provider records. See DATA_LICENSE.md, data_availability/source_provenance_license_matrix.csv, and data/provenance/UPSTREAM_VERSION_LIMITATION.md. This boundary does not prevent exact reproduction of the released fixed benchmark but does limit independent reconstruction of every historical upstream acquisition step.

## Verification steps

1. Run python scripts/verify_checksums.py after extracting the archive.
2. Run python scripts/verify_open_release_integrity_v1.py to validate public assets and the 275 archived comparisons without inference.
3. Run src/evaluation/evaluate_score_matrix_v1.py on any archived score matrix.
4. Optionally run src/evaluation/export_frozen_test_scores_v1.py in a compatible PyTorch environment to regenerate all frozen scores and compare the 275 metrics.
