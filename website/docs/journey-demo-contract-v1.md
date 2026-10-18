# PayGod Journey Demo Contract v1 (NON-CANONICAL)

Status: **Experimental / synthetic / not a PayGod Kernel contract**.

## Scope and trust boundary
This contract describes only the isolated website demonstration at `/journey/` and `/journey-check/`. It does not define a production Evidence Bundle, Warrant, policy decision, signature, issuer trust, release authorization, or Kernel canonicalization. The sample data is public and predictable. A successful recomputation is **integrity consistency**, not authenticity, authorization, time validity, or replay resistance.

## JSON fields
All fields are mandatory, and unknown fields are rejected by the independent CLI:
- `format`: literal `paygod-journey-demo-v1`
- `bundle_id`: literal `DEMO-EVB-001` (display identifier, **not** content-derived)
- `payload`: exact UTF-8 synthetic fixture (or its defined tampered variant)
- `baseline_payload`: exact synthetic fixture
- `scenario`: one of `clean`, `tamper`, `auth`, `demo`
- `outcome`: scenario-specific literal
- `evidence_sha256`, `decision_sha256`, `receipt_sha256`: lowercase hexadecimal SHA-256 strings of 64 characters
- `synthetic`: boolean `true`
- `executable`: boolean `false`

## Exact preimage and encoding
The current browser demo uses UTF-8 of the exact JavaScript string; it does **not** hash canonical JSON. The fixture is:

```text
PayGod demo payload | bundle DEMO-EVB-001 | amount_minor=1000 | policy=demo-v1
```

For scenario `tamper`, the observed payload appends ` | altered`. All other scenarios use the unchanged fixture.

`encode(fields)` joins `String(value).length + ':' + value` with `|`, where all current fields are ASCII. This length is JavaScript UTF-16 code-unit length, **not a general UTF-8 byte length**. For this strictly ASCII-only v1 fixture, the lengths coincide. Non-ASCII values are unsupported; do not generalize this scheme without an ADR and a cross-language specification.

```text
evidence_sha256 = SHA256(UTF8(payload))
decision_sha256 = SHA256(UTF8(encode([
  "paygod-demo-decision-v1", bundle_id, evidence_sha256,
  scenario, outcome, "synthetic-only"
])))
receipt_sha256 = SHA256(UTF8(encode([
  "paygod-demo-receipt-v1", bundle_id, evidence_sha256,
  decision_sha256, outcome, "not-signed"
])))
```

This is an educational deterministic digest chain, not a digital signature. A party who changes a payload and recomputes every digest can still make a self-consistent chain; therefore **digest matching alone is not tamper-proof provenance**.

## Negative tests
- Change `outcome` without recalculating hashes: reject.
- Change `payload` without recalculating hashes: reject.
- Change `bundle_id`, `scenario`, `format`, `synthetic`, or `executable`: reject.
- Add unknown keys, omit fields, or change hash casing/length: reject.
- Recompute a completely forged self-consistent chain: may pass *hash consistency*, but must never be treated as authenticity or release authority. This demo CLI restricts scenarios and fixtures, but those constants are public.

## Next boundary
Before using actual PayGod records: map Kernel-owned identifiers and receipt fields, define canonical bytes and versioning in an ADR, add issuer/signature/trust-root and authority verification, test time/replay separately, and obtain independent review. Do not change frozen evidence.
