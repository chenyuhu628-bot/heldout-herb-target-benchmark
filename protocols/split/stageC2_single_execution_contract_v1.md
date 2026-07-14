# Stage C2 single-execution contract v1

Status: FROZEN_INPUT_CONTRACT, documented in package-relative form for the v1.2 public reproducibility release.

## Historical permitted inputs

1. protocols/split/herb_split_blocking_group_members_v1.csv
2. protocols/split/herb_benchmark_eligibility_v1.csv
3. protocols/split/herb_benchmark_quarantine_v1.csv
4. protocols/split/group_split_features_pre_split_v1.csv
5. protocols/split/benchmark_positive_herbs_pre_split_v1.csv
6. protocols/split/group_aware_split_protocol_v1.json
7. protocols/split/group_aware_split_seed_derivation_v1.json
8. data/provenance/corrected_full_herb_target_positive_universe_v1.csv
9. data/provenance/clean_nodes_round5_fix8_identifier_harmonized_v4.csv
10. Historical herb-compound profile information represented by split-provenance files in this package
11. Historical freeze manifest not included because it contains local execution paths; see the public input list and provenance hashes instead

## Historical execution rules

At historical Stage C2 execution, one derived seed generated exactly one split. The process did not compare actual alternatives, read formal_v6 partitions, or run a model. The split was frozen immediately after hard-invariant validation, and the test labels were then transferred to a sealed payload.

In v1.2, those fixed labels are public for reproducibility and independent evaluation. Their publication does not change the historical split construction, but they are no longer an ongoing blinded test and remain ineligible for model selection, tuning, checkpoint selection, or post-test adaptation.

A historical rerun would have been allowed only after a hard-invariant failure or code error and would have retained the same seed, input hashes, ratios, features, and protocol. Soft balance, target coverage, validation performance, and test performance did not authorize a rerun.
