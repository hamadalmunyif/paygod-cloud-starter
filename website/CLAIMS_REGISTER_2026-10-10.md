# Canonical Kernel Website Claims Register — 2026-10-10

Status: **EDITORIAL RELEASE REVIEW — NOT A NEW SECURITY AUDIT**

This register supports `/explore/` and `/ar/` in the PayGod website proposal. The public technical source is **only** [paygod-kernel-mvp](https://github.com/hamadalmunyif/paygod-kernel-mvp).

## Publication rule

The public site may present a claim only if its functionality or scope is documented in the canonical Kernel repository and (for operational claims) has a named corresponding witness there. Research performed outside the canonical repository is **not a delivered Kernel feature**, and no external research repo is presented as another technical project on the site.

| Public claim | Canonical supporting material | Limit |
|---|---|---|
| Deterministic Kernel policy execution | [README](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/README.md), [START_HERE](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/START_HERE.md), [vectors](https://github.com/hamadalmunyif/paygod-kernel-mvp/tree/main/spec/test-vectors) | Requires represented and admitted input; not third-party fact truth |
| Portable integrity verification | [Standalone Verifier](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/STANDALONE_VERIFIER.md) | Hashes/receipt/ledger/bundle binding, not replay or historical original issuance on its own |
| Recipient-key Ed25519 receipt authentication | [Issuer Authenticity](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/ISSUER_AUTHENTICITY.md) | Does not confer a regulatory or contractual mandate |
| Single canonical decision path for registered adapters | [Repository Boundary](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/REPOSITORY_BOUNDARY.md) | Does not cover arbitrary unregistered or external rails |
| Pre-kernel evidence admission `WITHHELD`, orchestration `NOT RUN` | [ADR 0003](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/adrs/0003-evidence-admission-before-decision-execution.md) | Not a tri-state Kernel DSL or decision verdict |
| Full coherent bundle re-authoring requires independent receipt commitment for identity comparison | [Internal Verification Challenge](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/INTERNAL_VERIFICATION_CHALLENGE.md) | Receipt pin needs independent trusted delivery for source authentication |
| `paygod-c14n-v1` safe-integer contract | [Verifier contract](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/STANDALONE_VERIFIER.md) | No production decimal-heavy temperature or environmental profile demonstrated |
| Real B2 readiness remains open | [B2 Report](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/rehearsals/gas-site-readiness/b2/READINESS_REPORT.md) | 0/10 real/deidentified qualifying cases, 0/5 independent nondeveloper recipients; no validated willingness to pay |
| Open-Core and contribution pathways | [License](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/LICENSE), [Contributing](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/CONTRIBUTING.md), [Stop-Build](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/STOP_BUILD_RULE.md) | No shipped hosted enterprise SKU, SSO/RBAC, billing or regulatory certification |

## Excluded from the public capability list

- Local experimental warrant/E1/E2/S0/controlled-provider results and attack-catalogue numbers.
- Assertions of independent institutional or public-chain enforcement.
- AP2 / ACP / x402 protocol originality or live payment settlement.
- Other GitHub project identities, research taxonomies, or experimental partner integrations.
- Future hosted SaaS, enterprise features, paid subscription thresholds, or investment valuation assertions.

Unapproved source evidence may inform research, but **only canonical Kernel-adopted evidence** may enlarge the public capability list.

## Release gate

1. Confirm canonical Kernel docs and accepted claims at the release commit.
2. Require GitHub tests: site build, Arabic RTL + English LTR structural checks, existing browser verifier v0.4 regressions, standalone Python parity, and an assertion that only the Kernel repository is linked as source.
3. Review both locales on mobile and desktop; a CI-green markup test is not a visual/a11y certification.
4. Preserve `/verifier/` and offline download unchanged.
5. Keep PR #4 draft and `paygod.net` production alias unchanged until approval.
6. After Kernel's pending documentation reconciliation PR is accepted and merged, review all new wording again before promoting site copy to production.

The website presentation is a derivative of the **accepted Kernel implementation and its documented limits**, not a second source of execution truth.
