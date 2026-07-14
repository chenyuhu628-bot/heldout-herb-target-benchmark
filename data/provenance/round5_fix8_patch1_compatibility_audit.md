# round5_fix8 patch1 compatibility audit

## Main high-strict-only branch

- Relation set remains herb-target supervision plus herb-compound and high-strict compound-target context at future graph-build time.
- It does not load `target_interacts_target`; patch1 does not alter this branch.
- Frozen herb-compound and compound-target relation hashes are unchanged: `True`.

## Target-context sensitivity branch

- Must load only `normalized_target_target_context_round5_fix8_patch1.csv` or the normalized relation in the patch1 combined table.
- Must reject the base 4,963-row relation.
- Must call `round5_fix8_patch1_target_context_serializer.serialize_target_context` exactly once.
- The serializer emits 5,072 unique unit-weight arcs, does not create self-loops and forbids any second reverse expansion.
- Source occurrence counts and reciprocal provenance are audit metadata only and are not attention/message weights.

## Historical builders

- Existing formal_v4/formal_v5 builders were not modified and are historical only for target-context use.
- Their manual reverse-expansion behavior is incompatible with the patch1 serialized edge-index preview.

## Frozen artifacts

- Compound raw feature shape: `[1042, 1024]`; hash unchanged.
- Target raw sequence feature shape: `[2309, 25]`; hash unchanged.
- Positive universe count/hash were checked from the active custodian manifest only; pair content was not read.
