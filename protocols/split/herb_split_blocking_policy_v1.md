# Herb split-blocking policy v1

## Frozen policy

`SBLK_V1 — exact normalized standardized-name blocking`

P1 and P2 produce identical membership for all 1,247 herbs. Exact standardized-name equality is selected because it is the simplest transparent rule; additional node-name, pinyin, and Latin evidence does not change frozen component membership.

## Blocking edge

Two herbs receive a blocking edge only when both `normalized_standardized_name` values are non-empty and exactly equal.

## Group formation

- Take connected components of exact-name edges.
- Exact equality is transitive; each multi-member component must contain one normalized standardized name and be a clique.
- Herbs without an exact-name partner form singleton groups.
- Group IDs are `HBG_` plus the first 12 SHA-256 characters of sorted member herb IDs joined by newline.

## Scientific meaning

The group is a `split-level conservative identity/source-species blocking unit`. All member herbs must be assigned to the same future partition.

It does not mean confirmed duplicate records, confirmed same medicinal material, node merge, label merge, feature merge, or canonical ontology equivalence. Different medicinal parts, processing states, and preparations retain independent herb IDs.
