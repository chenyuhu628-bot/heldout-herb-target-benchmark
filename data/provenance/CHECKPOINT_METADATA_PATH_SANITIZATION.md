# Checkpoint metadata path sanitization

The copied historical best-checkpoint files contained machine-local absolute paths in metadata input-hash keys. Before this public release, those metadata path strings were replaced with portable historical_provenance identifiers.

Only checkpoint metadata paths were changed. The model state_dict tensor content was fingerprinted deterministically before and after each rewrite. The package checkpoint SHA-256 values therefore differ from the historical sealed serialization SHA-256 values, while the state_dict content fingerprints are unchanged.

For each of the 25 checkpoints, data/provenance/checkpoint_metadata_path_sanitization_v1.json records:

- the historical sealed serialization SHA-256;
- the released package serialization SHA-256;
- the state_dict tensor-content SHA-256;
- the number of metadata path strings replaced.

The public integrity verifier checks that each released checkpoint matches both the package manifest and this provenance record and contains no Windows absolute-path or file URI token.
