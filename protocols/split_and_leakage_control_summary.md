# Split and Leakage-control Summary

The benchmark uses a held-out-herb design in which training, validation, and sealed-test herbs are separated at the herb level. Validation herbs support model selection and diagnostics. Sealed-test herbs support the final one-time aggregate evaluation.

Leakage control is expressed as a public boundary: held-out labels and target-attributable held-out records are excluded from the release, and aggregate metrics are reported without redistributing raw evaluation rows or prediction-level outputs.

Third-party raw source records remain outside this package and must be obtained from the original providers under their own terms.
