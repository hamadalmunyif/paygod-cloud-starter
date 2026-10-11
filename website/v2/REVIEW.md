# PayGod V2 — gated design preview

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
