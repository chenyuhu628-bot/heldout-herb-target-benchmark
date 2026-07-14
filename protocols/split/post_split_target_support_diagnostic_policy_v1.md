# Post-split Target-support Diagnostic Policy v1

Status: `PREREGISTERED_BEFORE_TARGET_SUPPORT_IS_OBSERVED`

After Stage C2 freezes one split, diagnostics may count unique positive targets by
side, whether validation/test positives use targets observed in train positives,
seen-target versus unseen-in-train-target positive counts, and target support
frequency. These are diagnostics only.

Target identity cannot assign or reassign groups. Train target coverage cannot justify
a new seed. Test targets cannot be removed, and target coverage cannot change test
membership. Formal reporting may include all-target evaluation, a train-supported-
target subset, and target-support-stratified diagnostics, while the primary protocol
and membership remain unchanged.
