# Historical reference metrics

The files in this directory record metrics calculated during the historical one-time sealed evaluation, before the fixed test labels were public.

historical_test_metrics_by_checkpoint_v1.csv is a portable, path-sanitized reference used by the public frozen-score exporter. It must not be interpreted as a new evaluation after opening the test set. The public reproduction outputs are in results/metrics, including historical_metric_reproduction_comparison_v1.csv.

Its checkpoint_sha256 column is explicitly historical: it identifies the pre-release sealed checkpoint serialization before metadata paths were redacted. released_package_checkpoint_sha256 identifies the portable checkpoint included in this package. The two serializations have identical state_dict tensor-content fingerprints as recorded in data/provenance/checkpoint_metadata_path_sanitization_v1.json.
