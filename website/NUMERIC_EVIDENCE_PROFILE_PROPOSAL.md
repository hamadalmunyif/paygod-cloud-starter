# Fractional External Measurements: an Admission Research Note

Status: **NOT IMPLEMENTED / NO KERNEL SEMANTIC CHANGE** (2026-10-10).

The canonical source for current behavior is **only** [PayGod Kernel](https://github.com/hamadalmunyif/paygod-kernel-mvp), especially the [restricted verifier/canonicalization profile](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/STANDALONE_VERIFIER.md), [ADR 0003](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/adrs/0003-evidence-admission-before-decision-execution.md) and [Stop-Build](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/STOP_BUILD_RULE.md).

`paygod-c14n-v1` accepts safe integers in JSON, but not decimal/exponent numeric syntax or unsafe integers. A temperature, emissions factor or quantitative input that does not meet this contract must not be silently truncated or coerced to allow Kernel execution.

## Candidate admission-layer strategy, not a shipped profile

Preserve the original external bytes separately with their claimed source/time and a cryptographic commitment. Under a future frozen metric contract, derive an integer plus unit and scale, with declared precision, range, signedness and rounding behavior. Reject values that cannot be represented faithfully. The externally acquired original must remain available for subsequent review.

Illustrative—not live CEMS data:

| Raw value | Candidate representation | Meaning |
|---|---|---|
| 23.7 °C | `{"quantity":237,"unit":"degC","denominator":10}` | 23.7 °C |
| 0.184 kgCO2e/kWh | `{"quantity":184000,"unit":"kgCO2e_per_kWh","denominator":1000000}` | 0.184 kgCO2e/kWh |

This is only a sketch: the field names above are not a public versioned Kernel schema.

## Required evidence before promotion

1. Versioned metric/field specification and admissible source.
2. Lexically precise decimal parsing, explicit rounding/overflow/invalid-value policy, tested bounds.
3. Input byte commitments and source-label preservation.
4. Negative test vectors and independent recipient interpretation.
5. Confirmation no change to frozen `paygod-c14n-v1`, receipts, digests or policy truth-values.
6. Approved ADR/governance if any frozen Kernel primitive actually needs to change.

The production website must not market a general decimal, emissions or cold-chain measurement adapter until the canonical Kernel repo accepts, implements and tests such an interface. Experimental evidence is not automatic product acceptance.
