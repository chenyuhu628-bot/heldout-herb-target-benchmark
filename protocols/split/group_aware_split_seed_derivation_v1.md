# Group-aware Split Seed Derivation v1

Status: `SEED_DERIVATION_FROZEN`

## Exact Seed Material

```text
TCMRGAT_GROUP_AWARE_SPLIT_V1
5d31e47e333e23c6664289930d2f8d6d2e57ae9c48cab324484e78d824f2f939
2a4dac118d7c9f61c335d5a07fd5ec718ba49bc3a8c12698c6b060d0bfae13f2
780e4e227878cea3b442f324a3aef420885532089796942f636579dfcbd28503
babf11b8f801eb4a8de179cf34bde320e174b7e442e0d32c08d92a6357aea508
```

The block contains five LF-delimited lines and no trailing LF for hashing.

## Recalculation

1. Encode the exact seed material as UTF-8.
2. Compute SHA-256: `0ee00ff34b99bd4c2d8a1164e4c10ef303ed86b6bf320d61f7252b0180c15760`.
3. Take the first eight hexadecimal characters: `0ee00ff3`.
4. Convert them to unsigned integer: `249565171`.
5. Compute `249565171 % 2147483647 = 249565171`.
6. If the result were zero, use `2147483646`; this replacement was not required.

Derived integer seed: `249565171`

Stage C2 must use this seed exactly once. No date seed, formal_v6 seed,
multi-seed restart, seed search, or outcome-driven replacement is permitted.
No split was generated during this derivation.
