# PayGod V2 — historical preview review (retained)

**Current status, 2026-10-14:** V2 was subsequently promoted to the canonical EN/AR homepage in Cloud PR #12. The draft/preview-only descriptions below are retained as historical review instructions, not the present publication state. The new EIK developer pages proposed on PR #13 remain subject to separate review, release and live-domain verification.

Status: **design experiment only**. Source branch: `website/v2-gold-evidence-preview-20261011`. PR #10 is a **draft** against `website/paygod-production`. Never merge or promote this revision without explicit visual and technical approval.

## What is included

| EN | العربية | Purpose |
|---|---|---|
| /v2/ | /v2/ar/ | New PG brand concept and clickable/sliding evidence path |
| /v2/how-it-works/ | /v2/ar/how-it-works/ | Observe → evaluate → package → transfer → check |
| /v2/use-cases/ | /v2/ar/use-cases/ | Real Kernel Pack file/test links (GHG, CVE, ISO 27001) |
| /v2/atlas/ | /v2/ar/atlas/ | Claim boundaries: integrity vs source truth, authority, time |
| /v2/verifier/ | /v2/ar/verifier/ | Styled wrapper around unchanged /verifier/ (v0.4, English controls) |

The V2 carousel supports arrow-button movement and mouse dragging, while the cards themselves are genuine links. Touch scrolling is native. The same locale switch goes to the corresponding page in the other language. All generated V2 pages are `noindex,nofollow` and use locally hosted CSS and JS.

## Evidence Lens and interactive source journey (October 11 revision)

- Home EN/AR: added an **Evidence Lens** with three explicit claims (portable bundle, canonical authority, CVE Pack) and two user-selectable views: STORY and PROOF. Each proof view links directly to named Kernel source/README/test documentation and displays limits. The lens is also shown on the EN/AR Evidence Atlas pages.
- Home and How-it-works EN/AR: a **six-station Pack journey** with three fixed real Pack examples: critical CVE, GHG Scope 1/2 and ISO 27001. Each station takes the reviewer to a real source/test/contract page. The six stations are fixture → source declaration → Pack policy → expected decision → verifier receipt contract → original unchanged verifier demo.
- The homepage's existing right-hand carousel now synchronizes the station selection in the Pack journey. Both controls remain independently accessible through buttons and explicit URLs.
- Clarification: test cases show *expected* outcomes only; this experience does **not** run the selected Pack, generate a new Pack-specific receipt, check a bank payment, or create an authority witness.
- No changes to the V2 URL mapping, canonical Kernel, or original v0.4 verifier.
- Required reviewer flow: switch STORY ↔ PROOF, inspect all 3 evidence tabs, exercise 3 Pack selectors × 6 stations, open real file links, test both locales and mobile/keyboard. Preview may require a logged-in Vercel account.

## Hard boundaries

- **Existing production paths and independent verifier source are not modified.**
- All V2 pages are new generated static files, and no new Kernel capability is implied.
- Source data truth, qualified timestamps, delegated payment authority, and policy correctness are NOT guaranteed by a generic integrity check.
- The Verifier v0.4 is embedded as the existing same-origin `/verifier/` page. Its technical controls remain English.
- The geometric PG concept has not completed trademark clearance.
- External links point to the existing public Kernel, not the private workflow Observatory.

## Approval gates

1. GitHub CI: existing viewer/verifier tests + `python3 tests/v2.py` pass.
2. Verify both locale links, all ten direct routes, and each of six slide destinations.
3. Visual QA: iOS Safari, desktop Chrome, RTL flow, keyboard focus, reduced-motion.
4. Confirm Vercel preview has real content (not a protected-deployment shell) with an authorized browser.
5. Review rights to the final PG monogram SVG before any production logo replacement.
6. Only after sign-off: consider cherry-picking/merging specifically approved V2 changes. **Do not auto-promote**.

## Reproduction

```bash
cd website
python3 -m pip install -r vendor/requirements-issuer-auth.txt
python3 build.py
python3 tests/v2.py
```

The original regression workflow also runs the legacy verifier, claims-alignment and bilingual checks.
