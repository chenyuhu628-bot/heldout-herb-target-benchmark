# Formal Model Selection Protocol v1

Stage D2 runs 5 models x 4 configs x 2 tuning seeds = 40 train/validation-only runs. Each run selects best epoch by validation macro AUPR. For each model/config, aggregate two seeds by mean macro AUPR, then mean macro AUROC, mean Recall@50, lower parameter count, and config ID. Each model selects one config independently. Failed runs remain reported; the grid is not expanded. Final work then runs 5 models x 5 final seeds = 25 fresh runs. Test access is allowed once only after all final checkpoints are frozen.
