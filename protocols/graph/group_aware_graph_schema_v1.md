# Group-aware Graph Schema v1

Herb, compound, and target nodes are frozen by the clean node universe. Raw context relations are herb_contains_compound (herb to compound), two compound-to-target relations, and canonical undirected target-to-target pairs. Materialization adds deterministic reverse arcs for message passing. Herb-target positives remain supervision labels and are never non-label edges. Holdout herbs attach only through label-free herb-compound context at inference. Pure context-only herbs and H0847 are excluded.
