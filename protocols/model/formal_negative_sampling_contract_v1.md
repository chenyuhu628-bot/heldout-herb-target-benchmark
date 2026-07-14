# Formal Negative Sampling Contract v1

Only train-known positives are used. Each train herb independently samples a unique 1:1 set from all 2,309 targets excluding its train-known positives. Run seed and epoch determine sampling. No holdout labels, redistribution, duplicates, or capacity masking are allowed; deficit is a hard error.
