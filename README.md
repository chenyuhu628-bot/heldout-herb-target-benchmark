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

The previous archived release, `v1.0.1-submission`, is available through its [GitHub release](https://github.com/chenyuhu628-bot/heldout-herb-target-benchmark/releases/tag/v1.0.1-submission) and [Zenodo record](https://zenodo.org/records/21287303), version DOI [10.5281/zenodo.21287303](https://doi.org/10.5281/zenodo.21287303). The concept DOI [10.5281/zenodo.21287302](https://doi.org/10.5281/zenodo.21287302) resolves to the Zenodo record across versions. This submission refresh does not state a new Zenodo version DOI before Zenodo creates one.

Please cite the repository metadata in `CITATION.cff`. Manuscript citation details should follow the final published article once available.

## Source Provenance

Herb-related records used for Benchmark v1 were obtained from Dryad, DOI [10.5061/dryad.wh70rxwx9](https://doi.org/10.5061/dryad.wh70rxwx9), version 6. The Benchmark v1 herb-target source file was byte-identical to the Dryad-distributed file, which contains 89,775 data rows and has SHA-256 `a8087d72de7306fbbeeedf274069af9e78800406da3a6dedf6e97311adfab868`.

Dryad documentation attributes the herb-target and herb-compound records to HIT 2.0. HIT 2.0 is therefore retained as upstream attribution rather than as the direct source of the Benchmark v1 files.

## Licence

Project-authored code is released under the MIT License. Project-authored documentation, figures, aggregate metrics, figure/table source data, protocols, and public audit summaries are released under CC BY 4.0 unless otherwise stated. Third-party raw source records are not redistributed in this repository. Users must obtain third-party source records directly from the original providers under the providers' own licences and access conditions.

## Data Availability Boundary

The public package redistributes project-authored code, documentation, aggregate metrics, table source files, figure source data, protocols, and public audit summaries. Third-party raw source records are not redistributed. Raw held-out labels, raw test positives, target-attributable held-out records, score matrices, prediction matrices, model checkpoints, and controller-held materials are not included.

Contact: Chenyu Hu, chenyuhu628@gmail.com
