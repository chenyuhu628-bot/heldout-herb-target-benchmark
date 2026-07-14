# Upstream-version reconstruction limitation

This package is sufficient for exact re-evaluation of the released frozen benchmark. It contains the frozen graph representation, partition and label artifacts, candidate target order, selected weights, score matrices, and integrity hashes needed for that purpose.

It is not a complete historical reconstruction of every upstream provider extraction. In particular, the archival materials available for this project do not preserve an exact historical ChEMBL release identifier and every original target-target filtering decision in a form that can be re-executed against the providers. The package therefore does not substitute a current provider download and label it as the historical source snapshot.

This distinction has two consequences:

1. A reader can reproduce the released rankings and benchmark metrics exactly from the frozen package.
2. A reader cannot claim to have independently reconstructed the full original upstream acquisition pipeline solely from this package.

The source-provenance summaries and mapping audits retained in this directory document the available evidence. Any future source reconstruction should be treated as a new analysis, should use provider versions explicitly recorded at the time of download, and should not be conflated with the frozen benchmark results.
