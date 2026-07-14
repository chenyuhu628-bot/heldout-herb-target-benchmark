# Label semantics and PU evaluation audit v1

Recorded herb–target associations are positives; every other candidate pair is unlabeled. A 1:1 set of unlabeled comparison pairs is sampled per herb for the training loss, but validation and test score every held-out herb against all 2,309 targets and do not sample evaluation negatives.

The resulting task is PU ranking. Macro herb-level AUPR is a defensible primary endpoint for unequal herb-level prevalence, while macro AUROC, Recall@K, NDCG@K, and MRR are complementary descriptive rankings. None is a measure against experimentally confirmed negatives. Missing positives, curation intensity, and target popularity can depress or inflate observed metrics and change apparent rank.

The D12 manuscript contains no dangerous assertion of true negatives, non-interacting pairs, experimentally validated negatives, discovered therapeutic targets, confirmed mechanism, or unseen-target prediction. Earlier risks were explicitly repaired. Required phrase guard: use **recorded associations**, **unlabeled comparison candidates**, **PU ranking**, and **shared candidate targets**. State that all metrics are conditional on a frozen observation process.
