# Graph context and feature leakage audit v1

## Materialization and query boundary

The training graph has 535 herb nodes, 3,886 total nodes, 38,160 directed non-label edges, 6,253 herb–compound pairs, 69,053 supervision pairs, and seven relation types. C3 reports no held-out herb in its node/edge index. Test queries comprise 67 new herb nodes attached through 588 frozen herb–compound pairs; they do not enter training message passing, create gradients, expose a herb-target label, or use an independent query-ID embedding. Every query is scored against all 2,309 targets.

## Features and transduction

Herb representations are means over allowed compound embeddings. Compound and target embeddings are trainable shared transductive parameters. There is no frozen external scientific feature asset, herb-ID embedding, ID hash, held-out herb-target feature, or label-derived query feature in the review-safe contract. The setting is therefore **transductive non-herb representation with inductive unseen-herb encoding**, not fully inductive graph learning.

## Residual subtle-leakage questions

The schemas establish label-free query construction, but aggregate evidence cannot prove row-level source independence. Compound–target context is ChEMBL-derived, while herb-target labels, herb-compound context, and target-target context are HERB-derived. Whether the latter target-target edges were constructed independently of full herb-target labels is `NOT_ASSESSABLE_WITH_REVIEW_SAFE_FILES`. This is a provenance limitation requiring a lineage table, construction pseudocode, source/version fields, and a controlled no-label-derivation audit. It is not an evidence-based leakage FAIL.
