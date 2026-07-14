# Post-test design change audit v1

**Conclusion:** `PASS`

D8 attests that it did not modify data, D7 metrics, model ranking, primary metric, raw labels, checkpoints, training, inference, or rescoring. D9 repeats the no-change boundary. D10 validation preserves HeteroSAGE rank 1, TCMRGAT rank 2, D7 metrics, and no-post-test-change. D12 performed manuscript revision only and reports no data/checkpoint/model/score access.

The post-D7 change is compliant manuscript reframing: architectural-superiority language was replaced with benchmark/protocol contribution; PU and transductive scope were clarified; validation-only ablations were bounded; and HeteroSAGE's first-place result was made explicit. This is correction of claims to match frozen evidence, not post-test model selection or post-test experimental design.

No model, seed, split, sampler, feature contract, checkpoint selection, primary endpoint, model set, or formal result was changed. No unfavorable model was removed and no secondary metric was promoted to redefine the winner.
