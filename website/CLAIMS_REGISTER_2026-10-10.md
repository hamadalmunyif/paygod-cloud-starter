# PayGod.net — Public Claims & Evidence Register (2026-10-10)

Status: WEBSITE EDITORIAL REGISTER — evidence links checked against GitHub source; **not a new independent audit or executed test**.

This register governs copy in the bilingual public atlas at `/explore/` and `/ar/`. It does not amend the canonical Kernel README, test protocols, or governance freezes.

## 1. Source and outcome vocabulary

Source-class labels describe **basis**, not verdict:
- `SOURCE_PROVEN`: a specified behavior/contract exists in linked source code or versioned source artifact. This by itself proves neither deployment nor runtime success.
- `DOC_CLAIMED`: a written claim, design, proposal or report not independently re-executed for this website review.
- `RUNTIME_OBSERVED`: behavior recorded in a named, time-scoped test/workflow witness. It does not generalize beyond its environment.
- `UNKNOWN`: missing/out-of-scope evidence.

Do not conflate these with the frozen T0 attack outcome vocabulary:
`REJECTED_AS_EXPECTED`, `BYPASS_OBSERVED`, `NOT_TESTABLE_UNDER_T0`, `HARNESS_DEFECT`. A harness defect is **never** a passing security result.

## 2. Source-controlled claims for the website

| ID | Claim on website | Evidence type | Primary anchor | Maximum defensible statement |
|---|---|---|---|---|
| PG-WEB-001 | Canonical Kernel evaluates packs deterministically and produces portable evidence artifacts. | SOURCE_PROVEN | [Kernel README](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/README.md), [START_HERE](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/START_HERE.md) | Canonical software capability within supported profile; **not** autonomous execution or evidence truth. |
| PG-WEB-002 | Standalone verifier checks hashes, manifest/receipt binding and ledger, plus optional detached Ed25519 issuer signature under external recipient trust. | SOURCE_PROVEN; CI as separately claimed by README | [Verifier contract](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/STANDALONE_VERIFIER.md), [Issuer authentication](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/ISSUER_AUTHENTICITY.md) | Integrity and optional key-based signature verification; **not** policy replay, delegated authority, source truth or trusted timestamp. |
| PG-WEB-003 | Controlled local T0 two-surface release witness closed. | RUNTIME_OBSERVED in frozen CI and bounded harness | [T0 closure record](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/main/docs/CONTROLLED_HARNESS_T0_CLOSURE_V0.md) | At the recorded frozen main commit, 98/98 tests, 13/13 declared E1 Gate Zero attempts rejected, and 23 positive post-flight checks. No bypass **observed under T0**, not universally impossible. |
| PG-WEB-004 | Live ACP remote observation can be captured and admitted in a shadow-only PayGod workflow. | RUNTIME_OBSERVED under named GitHub Actions runs | [Witness 001 result](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/main/docs/WITNESS_001_RESULT.md) | Initially fractional descriptor data rejected at paygod-c14n-v1; follow-up shadow run succeeded without creating ACP jobs or moving funds. |
| PG-WEB-005 | Observation Pack stores raw captured ACP CLI output bytes plus derived normalized.json and digest commitments. | SOURCE_PROVEN | [Observation Pack spec](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/main/docs/OBSERVATION_PACK.md), [Obs README](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/main/README.md) | Capture preserves received local acquisition bytes; **not** an independently authenticated HTTP wire packet or third-party time. |
| PG-WEB-006 | Evidence admission refuses silently mapping unavailable evidence to false, and stops before canonical Kernel run. | SOURCE_PROVEN architecture decision; simulated workflow witness | [ADR 0003](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/adrs/0003-evidence-admission-before-decision-execution.md), [B2 report](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/rehearsals/gas-site-readiness/b2/READINESS_REPORT.md) | `WITHHELD` and `NOT RUN` are **outside** Kernel; no kernel tri-state or new semantic. |
| PG-WEB-007 | An internally coherent replaced evidence bundle requires an independent receipt pin to detect replacement. | SOURCE_PROVEN in protocol; reported internal challenge | [Internal verification challenge](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/INTERNAL_VERIFICATION_CHALLENGE.md) | Do not turn internal consistency into original provenance. |
| PG-WEB-008 | B2 gas real-readiness is not completed. | DOC_CLAIMED readiness report | [B2 report](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/rehearsals/gas-site-readiness/b2/READINESS_REPORT.md) | **0/10** qualifying real/deidentified cases; **0/5** independent nondeveloper recipients. P0 is synthetic and counts as zero real cases. |
| PG-WEB-009 | AP2 collision/originality and institutional economics are open. | DOC_CLAIMED research plan | [Pass B protocol](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/main/docs/AP2_COLLISION_PASS_B_HANDOFF_V0.md), [reaction matrix](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/main/docs/AP2_COLLISION_OUTCOME_REACTION_V0.md) | Do not market Warrant v0 as a novel independent standard, do not imply external blind human Pass B completed. |
| PG-WEB-010 | Agent Failure Taxonomy is a mature public normative standard. | UNKNOWN / NOT ESTABLISHED | [Current taxonomy repository](https://github.com/hamadalmunyif/agent-failure-taxonomy) | Present only as early-stage possible community contribution. |

## 3. Documentation drift that must not become a product claim

- [Kernel Open Core Policy](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/OPEN_CORE_POLICY.md) describes a **commercial strategy** with `login`, `sync`, dashboard, RBAC, industry-specific HIPAA/FedRAMP packs, and native integrations. These are not verified repository features; do not publish as shipped.
- [DAA Integration Profile](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/DAA_INTEGRATION_PROFILE.md) describes Advisor/Judge but also says the Kernel executes transactions and lists hypothetical gateways and circuit breakers. The current Kernel README says downstream actors execute; don't repeat the old execution wording.
- Kernel docs `00_VISION.md`, `07_AGENTIC_SECURITY_PROFILE.md`, and `09_CROSS_BORDER_DATA_PROFILE.md` are placeholders, not implemented profiles.
- Website `website/README.md` and `website/DEPLOYMENT.md` contain earlier October 1/2 review-stage statements. Vercel inspection on 2026-10-10 mapped production `paygod.net` and `www.paygod.net` to `paygod-evidence-preview` production READY deployment based on `website/paygod-production@8532995`. Preserve dated history, add dated correction instead of rewriting prior witness records.
- Public website source, Vercel READY metadata and actual independent user browser functionality are different kinds of proof.

## 4. Boundary-preserving roadmap language

The site may describe:
- a candidate numerical evidence-admission representation with **explicit scale, unit, precision, provenance, and rounding**; not a released CoPco/CEMS profile;
- possible independent cross-system verdict comparison, recipient-policy snapshots and trusted time as **research**;
- possible payments, industry/environment, agent workflows and external verification pilots as **applications requiring separate domain validation**.

The site must not assert:
- an independent bank/PSP release integration, actual authorized crypto settlement or live asset custody;
- a regulated audit or compliance accreditation;
- a new cryptographic invention;
- proved institutional adoption, purchase orders, willingness to pay, or tokenization rights;
- valid financial/reliance judgment solely because the internal verifier output says VALID.

## 5. Investment-readiness logic

A technical contribution, a design-partner commitment, and a proof of market demand are distinct. Suggested progression:
1. Code/reproducibility: external party reproduces a selected falsifiable claim and signs a bounded report.
2. Compatibility: an external system submits a real/deidentified case under a frozen evidence-admission contract.
3. Operational pain: the counterparty states who owns the risk or signoff and contributes staff/test data/sandbox access.
4. Budget signal: observable committed resources or paid pilot.
5. Scale: different independent enforcers/recipients can interpret the *same* authority/evidence semantics without needing to trust the original producer's local verdict.

None of stages 3–5 has been established here. Evaluate optional open-core, hosted verifier, independent review methodology, contract/pack tooling, and observational connectors **as alternatives**, not one fixed thesis.

## 6. Website implementation scope

- Source: `website/src/atlas.html` (Arabic+English editorial pages with independently addressable static routes).
- `website/build.py` emits `/explore/` (English), `/ar/` (Arabic), while retaining the existing `/verifier/`, self-contained offline verifier, and legacy landing/producer demo.
- Neither Kernel nor Observatory code, schema, receipt, Warrant, trust store, canonicalization or domain DNS is changed.
- Preview stays `noindex,nofollow`; production SEO needs review and an approved merge/release.
- A drafted change is not a deployed production feature, and a Vercel READY preview is not an independent security audit.

## 7. Publication gate

Before approving merge, require:
- Python website build success and no missing output paths.
- Existing browser and Python verifier regression tests remain green (CI).
- Check Arabic RTL and English layouts on mobile and desktop.
- Confirm `/explore/`, `/ar/` and `/verifier/` links and no unexpected response-header noindex on public atlas routes.
- Re-check all numeric claims, code anchors and status timestamps against pinned records at the release commit.
- Human review of English and Arabic terminology.
- Preserve the current production alias until explicitly approved.