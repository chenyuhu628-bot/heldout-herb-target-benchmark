# Validation and final-training provenance

This directory records the validation-only configuration-selection chain and final-training summaries that led to the 25 archived best checkpoints.

Raw tuning checkpoints, last checkpoints, internal run logs, and local-path run registries are not included. The public archive instead supplies the fixed final best checkpoints through artifacts/checkpoints/checkpoint_manifest_v1.csv, with package-relative paths and SHA-256 hashes.

The selection records are historical. They document how the final checkpoints were selected before the fixed test was opened; they do not authorize any new selection using the public labels or score matrices.
