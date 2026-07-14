# A held-out-herb target-prioritization benchmark with prespecified leakage controls and compound-profile similarity diagnostics

**Authors:** Chenyu Hu and Xinyou Zhang

**Affiliation:** School of Intelligent Medicine and Information Engineering, Jiangxi University of Chinese Medicine, Nanchang 330004, China

**Corresponding author:** Xinyou Zhang (xinyouzhang@jxutcm.edu.cn)

## Abstract

### Background

Reliable evaluation of herb-target graph models is difficult because entity overlap, shared graph context, incomplete positive labels and post-test adaptation can inflate apparent performance on held-out herbs. We developed a held-out-herb target-prioritization benchmark with prespecified controls on selected leakage pathways. In this study, these prespecified controls comprised exact normalized-name blocking across partitions; restrictions on access to held-out herb-target labels and query-specific identity features; validation-based model selection; and restrictions on post-test adaptation. Before final evaluation, the protocol fixed target-identifier harmonization, split blocking, label-free query construction, complete ranking of 2,309 candidate targets, model-selection rules, random seeds, metrics and a single sealed-test analysis. This operational definition does not imply similarity-disjoint partitioning or complete independence from upstream source construction.

### Results

In the sealed test, HeteroSAGE achieved the highest mean macro herb-level AUPR (0.682663, sample SD 0.010937), followed closely by TCMRGAT (0.679919, sample SD 0.005636) and GCN (0.679086, sample SD 0.007807). The three means differed by less than 0.004 macro AUPR, and the top-ranked model changed across seeds; the ordering was therefore interpreted descriptively. Validation-only diagnostics identified compound-profile nearest-neighbor transfer as a strong heuristic comparator, suggesting that performance in this split was influenced by compound-profile similarity and the amount of recorded training support available for candidate targets.

### Conclusions

The benchmark provides a structured evaluation framework for held-out-herb target prioritization. It combines a frozen evaluation protocol, aggregate reproducibility materials and diagnostics that separate model-family comparisons from the effects of compound-profile similarity and recorded-label coverage. The leading graph models performed similarly under the sealed test, while validation diagnostics indicated that compound-profile similarity was an important source of predictive signal in the validation split. The findings apply to the prespecified information boundary rather than to similarity-disjoint or provenance-complete generalization.

## Purpose of this v1.2 open reproducibility release

This is the v1.2 open reproducibility release of the benchmark. It preserves the historical one-time sealed evaluation as a provenance event, but the fixed test split is now public in this package. The package contains the 67 test herbs, 8,632 recorded-positive herb-target pairs, 2,309-target candidate universe, frozen graph inputs, 25 selected final checkpoints, and their 25 complete score matrices.

Accordingly, third parties can independently calculate the reported metrics, inspect every ranking, and evaluate compatible external score matrices against the same fixed test set. This public fixed test set is no longer a blinded or ongoing held-out test; it must not be used for model selection, hyperparameter tuning, checkpoint selection, or post hoc method development.

No retraining, tuning, model selection, or replacement of checkpoints was performed to make this release. The archived score matrices were regenerated from the 25 frozen checkpoints after release preparation and matched the historical sealed-evaluation reference metrics within absolute and relative tolerances of 1e-6.

## Contents

- data/splits: frozen partition registries, split diagnostics, and graph-isolation records.
- data/labels: public fixed-test positive pairs and the label-release manifest.
- data/graph: frozen graph snapshot, public test-query context, and candidate target order.
- artifacts/checkpoints: 25 fixed best checkpoints and their SHA-256-verified manifest.
- artifacts/scores: 25 complete raw decoder-logit matrices, one per frozen checkpoint.
- results/metrics: independently reproducible fixed-test metrics and the historical comparison.
- results/validation: validation-only tuning and final-training provenance.
- src/frozen_d1: byte-frozen feature, model, decoder, and metric implementations.
- src/evaluation: public score export and third-party score-matrix evaluation commands.
- protocols, audits, data_availability, and data/provenance: protocol, boundary, provenance, and licensing records.

The score matrices contain raw decoder logits, not calibrated probabilities. Rows correspond to the herb IDs stored in each NPZ file; columns correspond to the target IDs stored in that same file and in data/graph/candidate_target_universe_v1.csv. Consumers must not silently reorder either axis.

## Quick start

Use Python 3.12.13 or a compatible environment. The reference export was validated with PyTorch 2.6.0+cu124 and torch-geometric 2.8.0. See environment/README.md before installation.

To evaluate a supplied score matrix against the public fixed test:

    python src/evaluation/evaluate_score_matrix_v1.py ^
      --package-root . ^
      --score-matrix artifacts/scores/TCMRGAT__CFG04__FINAL_01_scores_v1.npz ^
      --output audits/generic_evaluator_smoke_TCMRGAT__CFG04__FINAL_01.json

On PowerShell, replace the caret line continuations above with backticks or place the command on one line.

To regenerate the 25 archived scores from the frozen checkpoints, without training or model selection:

    python src/evaluation/export_frozen_test_scores_v1.py ^
      --package-root . ^
      --device cuda:0 ^
      --query-batch-size 16 ^
      --verify-atol 1e-6 ^
      --verify-rtol 1e-6

The export command refuses a checkpoint or frozen-code mismatch and validates the generated metrics against results/reference/historical_test_metrics_by_checkpoint_v1.csv. It writes new outputs only when the chosen output location is empty, unless its explicit overwrite option is supplied.

## Independent evaluation route

For a model developed independently of this release, create an NPZ score file with all three arrays:

    scores: float64 or float32 matrix with shape (67, 2309)
    herb_ids: the exact 67 public test herb IDs in the archived order
    target_ids: the exact 2,309 candidate target IDs in the archived order

Then pass it to src/evaluation/evaluate_score_matrix_v1.py. The evaluator rejects a missing, duplicated, substituted, or reordered ID axis instead of correcting it implicitly. It produces herb-level macro metrics, micro metrics, ranking metrics, and per-herb results under the archived metric contract.

The public labels are recorded positives, not exhaustive biological truth. Reported metrics therefore quantify recovery of the archived positive records under this benchmark, not confirmed absence of all unlabelled herb-target relations.

## Historical and public-release scopes

The historical result columns in results/reference were calculated before the test labels were public. The public v1.2 score export is a post-release reproduction of those frozen checkpoints and metrics. It is evidence that the fixed assets reproduce the historical calculation; it is not a new blinded test and does not establish a new generalization result.

Supplementary Figure S2 illustrates this public independent-evaluation route. Historical review-safe audit records are retained only under data/provenance/legacy_audits and are explicitly superseded for access-scope statements by this README, data_availability, and audits/open_release_audit_v1.md.

## Data provenance and licensing

This package publishes a frozen derived benchmark snapshot, rather than redistributing all raw upstream provider records. The source-specific conditions and required attribution are documented in DATA_LICENSE.md, data/licenses/SOURCE_LICENSES.md, and data_availability/source_provenance_license_matrix.csv.

The code in src and scripts is licensed under the MIT License; see LICENSE and LICENSE_SCOPE.md. No blanket repository-wide licence is asserted for source-derived data, checkpoints, score matrices, or results. Reuse of those materials remains subject to the constituent source terms and the attribution/ShareAlike obligations described in the licence matrix.

For privacy, machine-local paths embedded in the copied checkpoint metadata were replaced with portable historical_provenance identifiers before this release. This changes the serialized checkpoint SHA-256 but not the state_dict tensor content. The source and released checkpoint hashes, tensor-content fingerprints, and path-sanitization counts are recorded in data/provenance/checkpoint_metadata_path_sanitization_v1.json.

## Integrity verification

After extracting a release archive, run:

    python scripts/verify_checksums.py

This verifies every package file listed in CHECKSUMS_SHA256.txt. The file MANIFEST.csv is a human-readable inventory. For a fuller audit of the test opening, fixed asset counts, and metric reproduction, see audits/open_release_audit_v1.md.

For a fast non-GPU check of the public labels, axes, checkpoints, 25 score matrices, and 275 historical-metric comparisons, also run:

    python scripts/verify_open_release_integrity_v1.py

## Citation

This release is archived on Zenodo at https://doi.org/10.5281/zenodo.21352219. Cite this version-specific archive, rather than the earlier v1.1 archive, when referring to the public test labels or score matrices. The code repository is https://github.com/chenyuhu628-bot/heldout-herb-target-benchmark.

## Important limitation

The package makes the frozen benchmark executable and independently evaluable. It does not reconstruct an exact historical upstream source snapshot for every third-party provider. In particular, an exact historical ChEMBL extraction version and every original target-target filtering detail were not retained. See data/provenance/UPSTREAM_VERSION_LIMITATION.md.
