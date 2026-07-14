# Dataset bias and label completeness audit v1

The benchmark evaluates recorded associations, not a complete interaction universe. Popular herbs and targets are more likely to be studied and curated; database inclusion and literature availability create observation bias; evidence quality varies across herb–target, herb–compound, compound–target, and target–target relations. Missing true positives are unavoidable, so an unrecorded pair cannot be treated as a true negative.

AUPR depends on recorded prevalence and can penalize plausible unlabeled predictions. AUROC can look optimistic in a large target universe and does not solve PU uncertainty. Recall@K, NDCG, and MRR describe where recorded positives appear in a ranking, not mechanism validation. All-target scoring removes sampled-evaluation-negative variance but does not remove curation bias.

Required manuscript language: the model prioritizes recorded associations for downstream investigation; metrics are conditional on a frozen observation process; performance may vary with herb degree and target support; no mechanism, therapy, efficacy, dose, safety, or clinical claim follows. Generalization is to held-out herbs under the same shared target/context universe, not to unseen targets, new databases, or all medicinal materials.
