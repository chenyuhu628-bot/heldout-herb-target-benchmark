# Sealed test integrity audit v1

**Overall:** `PASS`

| check | status | evidence |
| --- | --- | --- |
| D6 only outer SHA before test | PASS | D6 zip_opened=false; central directory/internal members not read. |
| D6 did not open payload | PASS | D6 internal_members_read=false and all label/metric flags false. |
| D7 opened after authorization | PASS | D7 opened_by_stage and operator record explicit authorization. |
| Container hash matched | PASS | D7 outer_sha256_matches_D6=true. |
| Test herbs = 67 | PASS | D7 ingest audit. |
| Positive pairs = 8,632 | PASS | D7 ingest audit; unique count also 8,632. |
| Candidate targets = 2,309 | PASS | D7 ingest audit. |
| 25 D3 final best checkpoints | PASS | D6 predeclared inventory; D7 formal run count 25 and primary summary says D3 frozen final best. |
| No D2 tuning checkpoint | PASS | D6 explicitly forbids; D7 summary identifies D3 best. |
| No D3 last checkpoint | PASS | D6 explicitly forbids. |
| No D4 ablation checkpoint | PASS | D6 explicitly forbids; D4 remains validation-only. |
| No C3 smoke checkpoint | PASS | C3 formal_initialization_allowed=false; D6 explicitly forbids. |
| No post-test tuning/model selection | PASS | D7 summary plus D8–D12 attestations. |
| Metrics frozen and ranks preserved | PASS | HeteroSAGE rank 1; TCMRGAT rank 2 across D7–D12. |

## Rebuttal-ready statement

Before test access, Stage D6 recorded only the outer SHA-256 of the opaque container and confirmed that no internal member or label was read. After explicit authorization, D7 verified the same outer hash, ingested 67 test herbs and 8,632 unique recorded pairs over the frozen 2,309-target universe, and evaluated the predeclared 25 D3 best-validation checkpoints exactly once. D2 tuning, D3 last-state, D4 ablation, and C3 smoke checkpoints were prohibited. Later stages changed only interpretation and release planning; the primary metric, values, and HeteroSAGE/TCMRGAT ordering remained frozen.

No sealed-test redo is required. A redo trigger would be an inventory mismatch, pre-freeze label access, hash mismatch, unauthorized repeat, or post-test reselection; none is present.
