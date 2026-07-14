# Data Availability statement for the v1.2 open reproducibility release

The frozen benchmark split, split and graph-isolation records, fixed public test labels, frozen graph inputs, candidate target universe, 25 selected final checkpoints, 25 complete raw decoder-logit score matrices, metric outputs, source data for figures and tables, provenance records, and verification utilities are available in the project repository and its version-specific Zenodo archive.

Repository: https://github.com/chenyuhu628-bot/heldout-herb-target-benchmark

Zenodo version-specific DOI: https://doi.org/10.5281/zenodo.21352219

The public fixed test set contains 67 herbs and 8,632 recorded-positive herb-target pairs, evaluated against 2,309 candidate targets. The labels are directly available in data/labels/test_positive_pairs_v1.csv; no access application is required. The public test set is no longer a blinded held-out test and must not be used for model selection, hyperparameter tuning, checkpoint selection, or post hoc method development.

Raw third-party provider records are not republished as a complete source-data mirror. Herb-related source records used for benchmark construction are available from the Dryad dataset “Comprehensive dataset of heterogeneous network structures in traditional Chinese medicine research” (DOI: 10.5061/dryad.wh70rxwx9). Compound-target context and target-identifier resources should be obtained from ChEMBL, HGNC, UniProt, and STRING under their applicable terms. Source-specific provenance and licence information are provided in data_availability/source_provenance_license_matrix.csv and data/licenses/SOURCE_LICENSES.md.

The archive supports exact re-evaluation of the released frozen benchmark, but it does not permit reconstruction of every historical third-party extraction. The limitation is documented in data/provenance/UPSTREAM_VERSION_LIMITATION.md.
