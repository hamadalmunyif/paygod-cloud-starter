# Website ↔ Kernel Parity Contract

Status: **PROPOSED / BOUNDED VERIFIER CONTRACT**  
Date: 2026-10-17

## Role of this repository

The website is a **recipient-side verification surface** for PayGod evidence. It may independently reproduce selected Kernel-defined canonical and transport checks, but it does not become a policy engine, evidence-admission gateway, receipt issuer, replay authority, trusted clock, or release/payment authority.

The canonical Kernel repository remains the source of protocol and decision semantics.

## Frozen canonical source identity

Observed canonical Kernel source:

- repository: `hamadalmunyif/paygod-kernel-mvp`
- observed compatible `main`: `203bee9ac5668975bf5248c57f922c214567d415`
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

These tests are valuable independent implementation evidence, but most are **website-local regression cases today**, not yet a single frozen cross-runtime corpus exported from the Kernel.

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

## Current limitation

The canonical shared corpus has 11 Kernel vectors. This supports a bounded statement such as:

> “The website verifier matches the pinned Kernel canonical corpus under the tested vectors.”

It does **not** justify:

> “The website fully implements the Kernel.”

The next promotion step is a versioned Full Parity Corpus shared unchanged across Kernel/.NET or reference tooling, standalone Python and browser JavaScript.

## Full Parity Corpus target

Promote independently:

1. canonical JSON;
2. ledger chaining;
3. manifest + bundle digest;
4. receipt binding;
5. external receipt commitment / coherent rewrite;
6. issuer signature + recipient trust-store cases;
7. negative transport mutations.

Keep replay, time authority, policy evaluation, evidence admission and mandate/authorization as separate dimensions rather than hiding them behind one `VALID` label.

## Deployment evidence is separate

GitHub test parity and Vercel delivery are different facts.

A production claim should correlate:

`exact GitHub source SHA → exact-SHA CI → Vercel deployment metadata → live smoke`.

PR #19 proposes adding a post-merge push-triggered exact-SHA website verifier witness. That PR does not itself authorize production, configure administrative branch protection, or enable PostHog.

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
