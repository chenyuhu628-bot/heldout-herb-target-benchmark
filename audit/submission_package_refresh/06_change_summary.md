# Submission package refresh

## Source branch and commit

Source branch: `main` at `a947f7145ff5b1a74520ea42515dbf99b496d4aa`.

## Dryad provenance corrections

Final-facing documentation now identifies Dryad version 6, DOI `10.5061/dryad.wh70rxwx9`, as the direct distribution source. It records the 89,775-row distributed herb-target table, its SHA-256 `a8087d72de7306fbbeeedf274069af9e78800406da3a6dedf6e97311adfab868`, and byte identity to the Benchmark v1 source file. HIT 2.0 is retained only as Dryad-documented upstream attribution.

## HERB wording retained only as background references

No final-facing file presents HERB as the direct Benchmark v1 source. Historical pre-change wording is retained only in the audit record.

## Figure 1 replacement

Replaced the canonical PDF and PNG with the supplied final Figure 1. The new figure contains Panels A-D, the final workflow and evaluation boundary, and the required visible values. No SVG file is required or added.

## Figure 3 replacement

Replaced the canonical PDF and PNG with the supplied final Figure 3. It preserves the supplied model ordering, primary AUPR values, descriptive differences, and the two selected secondary metrics. No SVG file is required or added.

## Obsolete files removed

None. No duplicate, preview, caption, or SVG file was present in the current branch.

## Figure 2 verification

Figure 2 is unchanged.

## README and provenance updates

Updated README, data availability, data licence, provenance matrix, Figure 1 source notes, and the benchmark summary terminology.

## Manifest and checksum updates

Updated Figure 1 and Figure 3 manifest roles. `CHECKSUMS_SHA256.txt` is regenerated after all refresh files are present.

## Zenodo DOI handling

The previous `v1.0.1-submission` archive remains explicitly labelled as previous. No new Zenodo version DOI is written.

## Remaining author decisions

Review the local diff and enter `APPROVE_PUSH_AND_RELEASE` before any commit, push, tag, or GitHub release is created.

## Files changed

Final-facing provenance, metadata, Figure 1 source notes, Figure 1 PDF/PNG, Figure 3 PDF/PNG, benchmark-summary terminology, manifest, and checksums.

## Files deleted

None.

## Files added

Audit records under `audit/submission_package_refresh/`.

## Scientific values unchanged

No training data, raw data, splits, sealed-test outputs, model metrics, or Figure 2 files are modified. Figure 3 source data is unchanged.
