# Group-aware Graph Isolation Protocol v1

Status: `FROZEN_BEFORE_SPLIT_CREATION`

## Training Graph

The training graph may contain herb nodes from train-assigned groups, allowed
herb-compound context within those groups, frozen compound/target/target-context
nodes and edges, and train herb-target supervision. It must exclude every herb node
and incident herb-context edge from validation and test groups, all context-only
excluded groups, validation labels, and test labels.

Within a train group, benchmark-positive herbs may provide supervision and
context-only members may remain as train-side context. Every herb remains a distinct
node; labels and features are never merged.

## Validation Evaluation

Validation herbs are wholly unseen during training. Their labels may support model
selection, but their groups cannot participate in training message passing. Validation
results cannot alter the frozen split.

## Test Evaluation

Test herbs are wholly unseen during training and model selection. Immediately after
split freeze, test labels were originally transferred to a sealed payload; v1.2 makes them public for reproducibility but not eligible for tuning. A single
formal test evaluation is allowed only after model and hyperparameters are frozen.
Its results cannot revise the protocol, sampler, model, seed, or split.

## Non-herb Nodes

This is unseen-herb inductive evaluation, not unseen-target evaluation. Compound and
target nodes may be shared across sides, and target-context edges may be shared. No
test herb or incident herb-context edge may enter the training graph.
