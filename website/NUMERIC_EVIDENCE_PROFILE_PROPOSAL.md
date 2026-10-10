# Proposed Numeric Evidence Admission Profile — NOT IMPLEMENTED

Status: RESEARCH PROPOSAL (2026-10-10). No kernel, schema, c14n or domain-pack semantics are changed by this file.

## Observed cause

The frozen `paygod-c14n-v1` canonicalization profile rejects JSON fractional/exponent numbers. Live ACP Witness 001 on 2026-10-06 encountered this exact admission mismatch and first failed closed. A later shadow-only run succeeded by preserving the external descriptor in the Observation Pack and passing a compatible bounded input into the canonical kernel. See [Witness 001 Result](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/main/docs/WITNESS_001_RESULT.md).

## Candidate adapter-level representation, not a default standard

Original acquired raw bytes must remain preserved and hash-bound outside any derived representation. A separate typed admission envelope MAY encode a physical measurement as a safe integer, with declared unit and scale.

**Illustrative transformation only** (not a verified CEMS reading):

| Raw external value | Candidate admitted representation | Interpretation |
|---|---|---|
| 23.7 degrees C | `{"quantity":237,"unit":"degC","scale_denominator":10}` | 237 / 10 °C |
| 0.184 kgCO2e/kWh | `{"quantity":184000,"unit":"kgCO2e_per_kWh","scale_denominator":1000000}` | 0.184 kgCO2e/kWh |
| 2.5 kWh | `{"quantity":2500,"unit":"kWh","scale_denominator":1000}` | 2.500 kWh |

## Admission prerequisites before any real pilot

- A frozen metric contract specifies base unit, denominator, allowable range, significant digits, and whether negative values are meaningful.
- Conversion parses the original decimal **lexically**, not through binary floating-point coercion; no rounding or truncation without an explicitly versioned rule and a `rounded` flag.
- Reject values whose numerator or denominator exceeds the safe-integer/canonical profile.
- Include input source identity as an **assertion with explicit provenance state**, not as automatically authenticated fact.
- Keep a cryptographic commitment to raw acquisition bytes and a versioned transformation code/spec digest.
- Preserve timestamp provenance separately: producer-supplied time ≠ trusted external time.
- Test unit mismatches, locale decimal comma, exponent formatting, missing values, NaN/Infinity, scientific instruments' calibration flags, and silent unit conversions.
- Only then admit eligible fields into a domain-specific pack; `WITHHELD` should prevent Kernel execution for missing mandatory fields.

## Why this is an adoption gap, not a Kernel defect

The current canonicalization rejects unsupported numbers as documented. Changing that global profile merely to accommodate temperatures or emission factors would change existing receipt/digest semantics. The correct next step is a separately reviewed representation/acceptance profile under the current stop-build rule, with a local test case demonstrating need and interoperability.

**Not claimed:** published CoPco or CEMS support, environmental certification, automated emissions calculation, or a live numeric-profile implementation.
