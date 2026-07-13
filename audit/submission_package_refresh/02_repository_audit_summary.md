# Repository audit summary

## Scope

The audit covered all tracked repository text files, source notes, manifests, checksums, public data-availability files, figures, and the current GitHub release metadata. The supplied final Figure 1 and Figure 3 PDF/PNG files were inspected as the replacement artwork. No SVG source or output is required for this refresh.

## Findings

- Two final-facing provenance locations incorrectly presented HERB as a direct source. They require Dryad version 6 wording and HIT 2.0 upstream attribution.
- Two final-facing locations used the obsolete `context-only` terminology for the 577 excluded source-asset herb records.
- The previous `v1.0.1-submission` Zenodo version DOI was present in current-facing metadata. It must be described only as a previous archive; this refresh must not state a new version DOI.
- Figure 1 and Figure 3 are replaced only at the existing canonical PDF/PNG paths. No duplicate figure, preview, caption, or SVG file was found in the repository.
- Figure 2 is unchanged.
- Remaining `primary ranking metric`, `MRR`, and `POP_PLUS_CT_PROP` matches occur in protocol or aggregate validation material and are retained without changes.

## Source-provenance standard

The final-facing source statement is: herb-related records were obtained from Dryad, DOI `10.5061/dryad.wh70rxwx9`, version 6. The Benchmark v1 herb-target source file was byte-identical to the Dryad-distributed file, which contains 89,775 data rows and SHA-256 `a8087d72de7306fbbeeedf274069af9e78800406da3a6dedf6e97311adfab868`. Dryad documentation attributes the herb-related records to HIT 2.0.

## Unresolved items

None for the repository-local refresh. A new Zenodo version DOI must not be added before Zenodo creates it.
