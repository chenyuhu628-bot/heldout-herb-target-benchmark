# Compound-target and target-context evidence audit v1

Confirmed aggregate facts include 1,456 high-strict ChEMBL-derived compound–target records, 8,835 additional included records from 9,431 inputs, and 4,963 included HERB-derived target–target source records after 24 composite exclusions. The audit specification records 2,536 normalized unordered target–target pairs. Evidence strata are described as source/support categories, not causal grades. D4 relation-removal and evidence-merging ablations are validation-only.

Two questions remain unresolved:

1. Compound–target edges are from ChEMBL rather than the HERB-derived herb–target supervision, which reduces direct same-table circularity, but release, filters, evidence semantics, joins, and row-level overlap are not fully documented.
2. Target–target context is HERB-derived. Review-safe aggregates do not prove it was constructed without using full herb–target labels or held-out co-occurrence.

Both are `NOT_ASSESSABLE_WITH_REVIEW_SAFE_FILES`, not FAIL. Add source release/access dates, exact relation definitions, evidence strata, normalization/deduplication, construction pseudocode, input/output hashes, and a controlled no-full-label-derivation audit. Do not claim that D4 establishes sealed-test component causality.
