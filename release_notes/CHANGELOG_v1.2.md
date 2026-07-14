# Changelog: v1.2 open reproducibility release

## Added

- Public fixed-test herb-target labels for 67 herbs and 8,632 recorded-positive pairs.
- Candidate target universe with the frozen 2,309-target order.
- Twenty-five selected final model checkpoints, fixed by SHA-256 manifest.
- Twenty-five complete raw decoder-logit matrices for all public test herb-target candidates.
- Public frozen-checkpoint score exporter and strict third-party score-matrix evaluator.
- Public-release audit, test-opening protocol, source-provenance licence matrix, environment instructions, and checksum inventory.
- Regenerated Supplementary Figure S2 showing the public independent-evaluation route.
- Path-sanitized checkpoint metadata plus source/release checkpoint hashes and state_dict fingerprints.

## Changed

- The former sealed test is now a public fixed test for reproduction and inspection.
- Data Availability documentation now distinguishes public fixed-test evaluation from historical sealed evaluation.
- Historical review-safe audits are retained only as legacy provenance and no longer define the current public-access scope.

## Not changed

- No model was retrained.
- No tuning, model selection, checkpoint selection, or post-test adaptation was performed.
- The released checkpoint metric outputs reproduce the historical sealed-evaluation reference within 1e-6 tolerance for all 275 checkpoint-metric comparisons.

## Known limitation

The package supports exact reproduction of the frozen released benchmark but not reconstruction of every historical upstream provider extraction. See data/provenance/UPSTREAM_VERSION_LIMITATION.md.
