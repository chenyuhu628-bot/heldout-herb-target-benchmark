# Release checklist for v1.2 open reproducibility

- The existing v1.1 Zenodo record remains intact. This v1.2 archive is a separate versioned release.
- Do not state a Zenodo version DOI in package metadata until Zenodo publishes the archive.
- Archive-level license choice: Other (Open) / source-governed. The package must not be described as uniformly MIT, CC0, or CC BY; see DATA_LICENSE.md.
- The final archive must pass `python scripts/verify_checksums.py` after extraction. Publish the archive checksum with the GitHub release.
- After Zenodo publishes the archive, cite its actual v1.2 version DOI when describing the public labels, checkpoints, score matrices, and evaluation code.

## Zenodo description

This version opens the fixed held-out-herb benchmark for reproducibility and independent evaluation. It contains public recorded-positive labels for 67 test herbs, a 2,309-target candidate universe, frozen graph inputs, 25 selected checkpoints, 25 complete score matrices, metrics, provenance, and verification utilities. The historical test was sealed before this release; after publication it is a public fixed test and must not be used for post hoc model selection or represented as a continuing blinded test.
