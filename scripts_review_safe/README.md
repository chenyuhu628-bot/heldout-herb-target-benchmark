# Review-safe Scripts

The scripts in this directory are review-safe utilities for checksum verification and aggregate figure-preview generation from public source data.

- `verify_checksums.py` validates every entry in `CHECKSUMS_SHA256.txt`.
- `plot_aggregate_figure_previews.py` generates aggregate figure previews from public source-data files and supports `--check-sources`.

These scripts do not access raw labels, do not access score matrices, do not rerun model training, and do not replace the final publication-layout figure files.
