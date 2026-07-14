# Release record for v1.2 open reproducibility

- The existing v1.1 Zenodo record remains intact; this release was created as its “New version”.
- Zenodo version-specific DOI: https://doi.org/10.5281/zenodo.21352219.
- Archive-level licence choice: Other / source-governed. The repository must not be described as uniformly MIT, CC0, or CC BY; see DATA_LICENSE.md.
- The final archive must pass `python scripts/verify_checksums.py` after extraction. The corresponding package checksum is published with the GitHub release and listed in its release notes.
- The manuscript Data Availability statement should cite this v1.2 DOI when describing the public labels, checkpoints, score matrices, and evaluation code. Confirm that the manuscript affiliation reads “School of Intelligent Medicine and Information Engineering” and that the uploaded supplement format matches the manuscript declaration.

## Suggested Zenodo description

This version opens the fixed held-out-herb benchmark for reproducibility and independent evaluation. It contains public recorded-positive labels for 67 test herbs, a 2,309-target candidate universe, frozen graph inputs, 25 selected checkpoints, 25 complete score matrices, metrics, provenance, and verification utilities. The historical test was sealed before this release; after publication it is a public fixed test and must not be used for post hoc model selection or represented as a continuing blinded test.
