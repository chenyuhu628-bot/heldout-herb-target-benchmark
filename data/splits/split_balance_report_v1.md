# Split Balance Report v1

Status: `OBSERVED_AFTER_SINGLE_FROZEN_EXECUTION`

## Positive Herbs and Groups

| Partition | Actual herbs | Target herbs | Abs deviation | Groups |
|---|---|---|---|---|
| train | 535 | 535 | 0 | 339 |
| validation | 67 | 67 | 0 | 67 |
| test | 67 | 67 | 0 | 67 |

## Positive Edges

| Partition | Pairs | Proportion | Abs deviation |
|---|---|---|---|
| train | 69053 | 0.79999305 | 0.00000695 |
| validation | 8632 | 0.10000348 | 0.00000348 |
| test | 8632 | 0.10000348 | 0.00000348 |

## Local Improvement

- Initial objective: `[0,0,"150614/431585","4650223/1255965","394/2365","a6f778cef58ac427fd9464b711d0ff7728fd4122baccd172701357a2573e0e8c"]`
- Final objective: `[0,0,"6/431585","138439963333/92708637820","394/2365","005c7a41d6775ba6e55d2cc523acc042bdc75f7cdea4a50efd6f00d7f8a65d0f"]`
- Accepted moves: 0
- Accepted swaps: 204
- Completed passes: 2
- Stopping reason: `FIRST_COMPLETE_PASS_WITH_NO_IMPROVEMENT`
- Final assignment signature: `005c7a41d6775ba6e55d2cc523acc042bdc75f7cdea4a50efd6f00d7f8a65d0f`

Degree-bin and group-size details are frozen in the companion CSV audits. Soft imbalance was not used for seed or mapping reselection.
