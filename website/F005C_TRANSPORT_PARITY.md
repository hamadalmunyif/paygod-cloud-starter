# F-005C — Kernel Portable Transport Parity

Status: **DRAFT / SHARED CORPUS TEST — NOT PRODUCTION AUTHORITY**

This branch consumes the exact Kernel-owned `paygod-transport-parity-v1` corpus.

Source:
- Kernel PR #125
- Kernel corpus blob: `d3e682cb7f4f82cc88c4b8fd3ec7fb99d53357da`

Website fixture:
- `website/tests/fixtures/kernel-transport-parity-v1.json`
- expected identical Git blob: `d3e682cb7f4f82cc88c4b8fd3ec7fb99d53357da`

The shared ten-case corpus covers bounded recipient verification behavior for manifest/artifact/bundle integrity, receipt/ledger binding, unexpected members, missing ledger, external receipt commitment, coherent rewrite, and recipient-supplied Ed25519 trust success/failure.

The website runs the corpus through:
1. browser JavaScript verifier;
2. vendored Python verifier.

Passing this corpus establishes **scoped transport verifier parity only**. It does not establish source truth, scanner completion, policy correctness, execution replay, trusted time, issuer mandate, payment authorization or release authority.

Merge order is intentionally separate: Kernel source corpus first, website ledger parity second, then this transport parity change. After every base change, require a fresh exact-head Website Verifier run before merge.
