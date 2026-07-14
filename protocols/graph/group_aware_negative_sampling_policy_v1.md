# Group-aware Negative Sampling Policy v1

Training negatives are sampled independently for each train herb at a fixed 1:1 ratio. Candidates are frozen clean targets excluding only that herb's train-known positives. Sampling is endpoint-conditioned and deterministic from run seed, epoch, and herb ID. No cross-herb redistribution, validation label, test label, sealed payload, or complete positive universe is allowed. A sampled pair is unobserved under train labels and is not asserted to be a biological negative.
