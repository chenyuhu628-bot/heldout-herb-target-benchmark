# Formal Node Feature Contract v1

Status: `FORMAL_FEATURE_CONTRACT_FROZEN`

The upstream manifests contain no frozen scientific node-feature asset: `NO_FROZEN_SCIENTIFIC_NODE_FEATURE_ASSET_FOUND`. Formal compound and target inputs are shared trainable embeddings in a transductive non-herb setting. Every train, validation, and test herb uses the same mean encoder over label-free compound context. There is no trainable herb-ID embedding, no random query-herb initialization, and no herb-target label in features. Missing herb context is a hard error. Embeddings use seeded Xavier initialization; LayerNorm is inside encoders. Feature dimension equals hidden_dim (64 or 128). Run seed affects initialization only. C3 deterministic ID-hash features are `ENGINEERING_SMOKE_ONLY` and forbidden from formal training, baselines, ablations, and manuscript results.
