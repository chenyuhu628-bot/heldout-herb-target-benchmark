# Pre-split Scientific Universe Audit v1

Status: `PRE_SPLIT_UNIVERSE_AUDITED`

## Clean Node Universe

- Rows processed: 4598
- Clean herbs: 1247
- Clean targets: 2309
- Other node types: {"compound": 1042}
- Blank node IDs: 0
- Herb ID unique: True (duplicate rows: 0)
- Target ID unique: True (duplicate rows: 0)

Only `node_id` and `node_type` were loaded.

## Positive Universe

- Selected columns: `herb_id`, `target_id`
- Raw rows: 87825
- Exact duplicate normalized non-empty pairs: 0
- Unique normalized non-empty herb-target pairs: 87825
- Unique valid herb-target pairs: 87825
- Unique positive-bearing herbs: 670
- Unique positive targets: 1894
- Herb IDs outside clean herb universe: 0
- Target IDs outside clean target universe: 0
- Rows with an empty ID: 0
- Rows with malformed non-empty ID syntax: 0

No pair table or target-ID list was exported.

## Benchmark Eligibility Filter

- Benchmark-eligible herbs: 1246
- Benchmark-ineligible herbs: 1
- Ineligible herbs other than H0847: 0
- H0847 excluded: True
- Positive pairs associated with all ineligible herbs: 1508
- Positive pairs associated with H0847: 1508
- Filtered unique valid positive pairs: 86317
- Positive-bearing eligible herbs: 669
- Benchmark-eligible herbs without a positive pair: 577

All counts are independently reconstructed from the frozen pre-split inputs. Any
deviation from earlier approximate expectations is resolved in favor of these
hash-frozen inputs and the explicit endpoint/eligibility rules above.
