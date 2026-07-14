# Split integrity and identity leakage audit v1

## Frozen facts

- SBLK_V1 uses exact matching after normalized standardized-name transformation.
- 1,247 herb records form 1,051 groups: 941 singleton groups and 110 multi-member groups containing 306 herbs; maximum group size is 9.
- Formal partitions contain 535/67/67 herbs and 339/67/67 groups for train/validation/test.
- Positive pairs are 69,053/8,632/8,632.
- 577 context-only herbs and quarantined H0847 are excluded from formal supervision.
- C2 reports groups and pair sets disjoint, non-train herbs absent from the train allowlist, H0847 absent, and formal_v6/old seal not read.
- C3 reports 535 training herbs and no validation/test herb in training nodes or edges.

## Assessment

`PASS` for the defined exact-name identity route and graph-node isolation. The split is sufficient to block observed exact normalized-name group overlap. It is not evidence of canonical medicinal-material equivalence and cannot exclude every taxonomic synonym, translational synonym, botanical-part relation, processed-product relation, or pharmacognostic near-equivalence. The D12 manuscript now states this boundary correctly.

## Redo decision

No split redo is required. Redo would be triggered by a verified cross-partition blocking group or normalized name, a validation/test herb in the training graph, H0847 positives in the formal benchmark, or reuse of formal_v6 split/results. All corresponding review-safe checks pass. The residual ontology limitation requires description and Supplement, not post-test repartitioning.
