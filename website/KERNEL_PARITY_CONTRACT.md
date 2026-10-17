# Website ↔ Kernel Parity Contract

Status: **PROPOSED / BOUNDED VERIFIER CONTRACT**  
Date: 2026-10-17

## Role of this repository

The website is a **recipient-side verification surface** for PayGod evidence. It may independently reproduce selected Kernel-defined canonical and transport checks, but it does not become a policy engine, evidence-admission gateway, receipt issuer, replay authority, trusted clock, or release/payment authority.

The canonical Kernel repository remains the source of protocol and decision semantics.

## Frozen canonical source identity

Observed canonical Kernel source:

- repository: `hamadalmunyif/paygod-kernel-mvp`
- observed compatible `main`: `8e1728dc8467964abef0e32967fea6f1bdf001f4`
- source corpus: `spec/test-vectors/canonical-json.json`
- exact source Git blob: `3880d3a45b417ae95cae9a7b8cebb1c8c47722d8`

Website fixture:

- `website/tests/fixtures/kernel-c14n-reference-20261014.json`
- exact fixture Git blob: `3880d3a45b417ae95cae9a7b8cebb1c8c47722d8`

The identical blob identity proves that the website parity test consumes the same frozen canonical corpus bytes. The moving Kernel branch SHA is recorded as provenance; the corpus blob is the exact shared-test identity.

## Current canonical parity

`website/tests/kernel_c14n_reference.mjs`:

1. computes the fixture Git blob and rejects silent fixture drift;
2. runs every shared Kernel canonical vector through the browser canonicalizer;
3. compares exact canonical bytes;
4. compares SHA-256 values;
5. requires shared bad vectors to fail closed;
6. separately rejects raw decimal, exponent and unsafe-integer number lexemes before JavaScript parsing can erase their lexical form.

This is **scoped canonicalization parity**. It is not full Kernel parity.

## Website verifier scope

`website/src/verifier.mjs` currently exercises recipient-side checks for:

- manifest file hash / byte-count integrity;
- unexpected member rejection;
- bundle digest;
- manifest ↔ receipt binding;
- locked ledger presence and chaining;
- receipt verdict / reason / rule binding to the locked ledger;
- Pack and input binding;
- external receipt commitment pinning;
- optional detached Ed25519 verification against a recipient-supplied trust store;
- explicit producer-clock status.

Tests include clean and mutation cases in the browser implementation and a standalone Python verifier.

Canonical, ledger and transport parity are now separated explicitly. Website-local regressions remain valuable, but the promoted parity claims below require exact frozen Kernel corpus identities rather than local cases alone.

## Verification dimensions

The website must continue to report dimensions separately:

| Dimension | Meaning |
| --- | --- |
| `integrity` | internal hashes/bindings/locked evidence are consistent |
| `issuer_authenticity` | detached signature result relative to recipient-supplied trust |
| `replay` | whether an execution was independently replayed |
| `time_authority` | provenance/strength of time evidence |

A transport may be internally valid while issuer authenticity is `not_verified`, replay is `not_performed`, and time is only `producer_supplied`.

## Explicit exclusions

The browser must not infer these from canonical or transport integrity:

- external source completeness or truth;
- scanner success/remediation semantics;
- `typed-v1` policy correctness;
- source admission under Kernel ADR 0003;
- issuer mandate / business authority;
- payment or release authorization;
- independent trusted timestamp;
- independent replay when no replay happened.

## Current bounded parity state

The website currently has three promoted shared-corpus witnesses:

1. **Canonical JSON parity** — Kernel/website fixture blob `3880d3a45b417ae95cae9a7b8cebb1c8c47722d8`.
2. **Ledger canonical/hash parity** — Kernel/website fixture blob `ac16a235641f22101dab93187af0eb992f010987`.
3. **Portable transport verifier parity** — Kernel/website fixture blob `d3e682cb7f4f82cc88c4b8fd3ec7fb99d53357da`.

The transport corpus contains ten shared cases covering clean/no-trust, trusted issuer, wrong trust key, payload tamper, unexpected member, receipt substitution, missing ledger, wrong external receipt commitment, coherent rewrite without a pin, and the same rewrite pinned to the original receipt.

PR #22 was merged after exact-head Website Verifier and Codex review. The parity/runtime merge established production source SHA `684610b7138f849406679b8d862ce701cc13fe4b` before this documentation PR. At that SHA:
- `website/paygod-production` pointed to the same SHA;
- push-triggered Website Verifier run `39068220184` completed SUCCESS;
- Vercel production deployment `dpl_FQjQhqBDEh9EJcPhKBk7Yovamqka` reported READY for the same Git SHA;
- canonical corpus parity passed;
- ledger corpus parity passed;
- browser transport corpus parity passed;
- vendored Python transport corpus parity passed;
- LF checkout enforcement passed;
- privacy telemetry contract remained not instrumented;
- existing browser and standalone Python regression suites passed.

This establishes exact-SHA source/CI/deployment correlation for that parity release. A live HTTP/browser smoke witness is still separate and was not established by these metadata/CI facts alone.

This supports bounded statements such as:

> “The website verifier matches the pinned Kernel canonical, ledger and portable-transport corpora under the tested cases.”

It still does **not** justify:

> “The website fully implements the Kernel.”

Keep replay execution, trusted time, policy evaluation, evidence admission, scanner/source truth and mandate/authorization as separate dimensions rather than hiding them behind one `VALID` label.

## Deployment evidence is separate

GitHub test parity and Vercel delivery are different facts.

A production claim should correlate:

`exact merged GitHub source SHA → push-triggered exact-SHA CI → Vercel production deployment metadata for the same SHA → live smoke`.

PR #19 is merged and the post-merge push-triggered exact-SHA verifier gate is active. PR #21 (ledger parity) and PR #22 (transport parity) were then merged in dependency order with fresh exact-head verification after each production-base change.

The last parity/runtime release before this documentation PR correlated GitHub production source, push CI, and Vercel production metadata at SHA `684610b7138f849406679b8d862ce701cc13fe4b`. Live smoke remains a separate required witness.

Merging this documentation PR will itself produce a new production SHA; therefore exact-SHA push CI and Vercel correlation must be checked again after this documentation-only merge before calling that new SHA release-correlated.

The production branch is currently observed as administratively unprotected, so future bypass resistance remains a governance item separate from the technical evidence above. This contract does not enable PostHog or confer production/payment/release authority.

## Change discipline

If the Kernel canonical corpus blob changes:

1. do not overwrite the existing website fixture silently;
2. preserve the old fixture for historical verification when required;
3. import/pin the new source explicitly;
4. run positive and negative parity;
5. preserve any divergence witness before repair;
6. update claim language only after evidence is green.

## Nonclaims

This document does not authorize a production deployment, prove institutional adoption, enable telemetry, accept Kernel ADR 0004, or claim source/issuer/release authority.
