# Group-aware Split Protocol v1

Status: `PREREGISTERED — NO ACTUAL SPLIT CREATED`

## Scope and Assignment Unit

The sole assignment unit is `split_blocking_group_id`; herb-level independent
assignment is forbidden. An eligible benchmark herb must be benchmark eligible,
carry at least one unique positive pair in the frozen positive universe, occur in
the clean herb universe, belong to exactly one blocking group, and not be quarantined.
Groups without a benchmark-positive herb are excluded from ratio calculations.

## Ratios and Fixed Features

Ratios are train 0.80, validation 0.10, and test 0.10. Largest remainder gives
integer positive-herb targets `535/67/67`.
Allowed features are group benchmark-positive-herb count, group positive-pair count,
D01-D08 counts, total group size, and the deterministic tie-break key. Target identity,
specific target distributions, compound identity, herb names, predictions, formal_v6
partitions, and test metrics are forbidden. Target identity may be inspected only as
a post-freeze diagnostic and can never change membership.

## Deterministic Ordering

Use seed `249565171`. For group `g`, the tie-break key is
`SHA-256("249565171|g")`. Sort assignable groups by benchmark-positive-herb
count descending, positive-pair count descending, total member count descending,
then tie-break key ascending.

## Lexicographic Objective

At every greedy decision and local-improvement candidate, minimize in this order:

1. Maximum absolute positive-herb-count deviation from frozen integer targets.
2. Sum of the three absolute positive-herb-count deviations.
3. Sum of absolute positive-edge proportion deviations from 0.80/0.10/0.10.
4. Sum of D01-D08 side-proportion deviations from 0.80/0.10/0.10.
5. Sum of group-count proportion deviations from 0.80/0.10/0.10.
6. Assignment signature.

Current greedy states use current counts against final integer herb targets, current
edges divided by all eligible edges, current bin counts divided by each global bin
count, and current group counts divided by all assignable groups. The signature is
SHA-256 over LF-joined `<group_id>=<side>` records sorted by group ID, with no trailing
LF; a partial greedy state includes assigned groups only.

## Initialization and Local Improvement

Run one greedy pass in frozen group order. Candidate side order is train, validation,
test; choose the complete lexicographic minimum. Then run deterministic single-group
moves followed by pairwise cross-side swaps. Traverse groups and group-ID pairs in
ascending lexical order and destinations in train, validation, test order. Update
immediately only on strict lexicographic improvement. One move traversal plus one swap
traversal is a complete pass. Stop on the first pass with no improvement or after 100
complete passes. No multi-seed restart, random search, or target-identity adjustment is
allowed.

## Hard Invariants

Each assignable group and each benchmark-positive herb occurs exactly once; groups
are indivisible; H0847 and pure context-only groups are absent; all three sides are
non-empty; validation and test each contain a group; no blocking group crosses sides;
and formal_v6 partitions are never used. Moves that violate an invariant are rejected.

Positive-herb, edge, bin, and group-count balance are soft objectives. Stage C2 is
executed once. If hard invariants pass, imperfect soft balance is not a reason to
replace the seed, rerun the algorithm, or hand-select a different split.
