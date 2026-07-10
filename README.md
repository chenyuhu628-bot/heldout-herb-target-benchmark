# Leakage-controlled held-out-herb target prioritization benchmark

This repository provides review-safe materials supporting a leakage-controlled held-out-herb target-prioritization benchmark.

It supports:

- inspection of frozen protocols
- inspection of aggregate sealed-test metrics
- inspection of validation-only diagnostic aggregates
- inspection of figure and table source data or source notes
- inspection of public provenance and audit summaries
- checksum verification
- review-safe reproduction of aggregate figure previews from public source data

It does not contain:

- raw held-out labels
- raw test positives
- target-attributable held-out records
- score matrices
- prediction matrices
- model checkpoints
- third-party raw source records
- controller-held materials

## Repository Structure

- `environment/`: minimal packages for review-safe checksum validation and aggregate figure-preview generation.
- `scripts_review_safe/`: checksum verification and aggregate figure-preview utilities.
- `protocols/`: frozen benchmark, split, metric, model-selection, and validation-diagnostic summaries.
- `figures/`: final main and supplementary figures plus public source data or source notes.
- `tables/`: main and supplementary table source files.
- `results_aggregates/`: aggregate metrics only.
- `audits_review_safe/`: public audit summaries.
- `data_availability/`: public/restricted material inventories, provenance matrix, and data-availability statements.

## Quickstart

1. Install requirements:

   ```bash
   python -m pip install -r environment/requirements_review_safe.txt
   ```

2. Verify checksums:

   ```bash
   python scripts_review_safe/verify_checksums.py
   ```

3. Generate aggregate figure previews from source data:

   ```bash
   python scripts_review_safe/plot_aggregate_figure_previews.py
   ```

   To check source-data presence and schema without writing preview files:

   ```bash
   python scripts_review_safe/plot_aggregate_figure_previews.py --check-sources
   ```

The preview-generation script reads only public files under `figures/source_data/` and writes local preview outputs to `aggregate_figure_previews/`. The final publication-layout figure files are the PDF and PNG files under `figures/main/` and `figures/supplementary/`.

## Citation

Please cite the repository metadata in `CITATION.cff`. Manuscript citation details should follow the final published article once available.

## Licence

Project-authored code is released under the MIT License. Project-authored documentation, figures, aggregate metrics, figure/table source data, protocols, and public audit summaries are released under CC BY 4.0 unless otherwise stated. Third-party raw source records are not redistributed in this repository. Users must obtain third-party source records directly from the original providers under the providers' own licences and access conditions.

## Data Availability Boundary

The public package redistributes project-authored code, documentation, aggregate metrics, table source files, figure source data, protocols, and public audit summaries. Third-party raw source records are not redistributed. Raw held-out labels, raw test positives, target-attributable held-out records, score matrices, prediction matrices, model checkpoints, and controller-held materials are not included.

Contact: Chenyu Hu, chenyuhu628@gmail.com
