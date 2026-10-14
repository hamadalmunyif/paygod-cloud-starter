# Paygod.net EN/AR EIK Developer Entry — release boundary, 2026-10-14

**Status:** proposed editorial/source update on branch `website/eik-bilingual-developer-entry-20261014`, not production proof. Never infer DNS/alias delivery from a repository PR or CI pass.

## Why this update exists
Kernel merged an actual bounded synthetic EIK reference in PR #112. Public website content must reflect that new *source-linked learning and compatibility path*, without implying that a user or external partner has implemented EIK commercially.

## Two new source-linked routes
- English: `/developers/`
- Arabic: `/ar/developers/`

Both present the same five concepts: what the public Kernel supports, where to learn, how to privately create a Pack, how to exercise synthetic admission→CLI→recipient verification, why upstream PR is optional, and what remains unproven.

The pages are editorial **not** runtime tooling, MCP/A2A endpoints, interactive YAML editors, CI control panels, source-attestation services, hosted Kernel execution, or release authorization. The separate existing `/verifier/` remains unchanged. Bilingual V2 homepages link to these routes and every V2 navigation shows a developer link; original `/v1/`, use cases, atlas and verifier remain intact.

## Public evidence pinned for editorial claims
- Kernel [PR #109](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/109) merged `cec36f268a3ddc0021ae9ea25a20ea6dbd929fdc` (AGENTS, private Pack onboarding).
- Kernel [PR #110](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/110) merged `ad4700fc90a3d620906ca0d7354cd4a0db2a40b5` (opt-in typed preflight).
- Kernel [PR #112](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/112) merged `248817e90c38cb2a077da36203d69bc4ea8ca994` (synthetic GitHub Actions reference).
- [Current EIK implementation limits](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/eik/STATUS_2026-10-14.md). Historical [claims register](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/CLAIMS_REGISTER.md) is a pinned older snapshot and remains preserved.
- [Issue #111](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/111): generic expression coercion and missing input admission remain separately unresolved.

## Acceptance before any domain promotion
1. **Source and exact head:** confirm PR changes only expected developer page source, bilingual V2 navigation/link, sitemap, docs and tests. Canonical Kernel and browser verifier unaffected.
2. **Protected GitHub CI:** production-mode site build and all current EN/AR home, atlas, use-case, verifier tests pass on exact PR SHA; new `tests/eik_developers.py` passes in preview and production build modes.
3. **Preview browser QA:** open both `/developers/` and `/ar/developers/` on a real Vercel preview. Inspect mobile/iPad Safari, desktop, keyboard, RTL, hreflang navigation and every link. Preview may require Vercel authentication.
4. **Launch control:** verify Vercel project `paygod-evidence-preview`, production branch `website/paygod-production`, root directory `website`, expected output and no unreviewed environmental/secrets change. A GitHub merge may trigger an actual production deployment; treat the release separately.
5. **Production smoke:** check `https://paygod.net/`, `/ar/home/`, `/developers/`, `/ar/developers/`, `/verifier/` and `/v1/`; verify the exact deployed commit SHA, HTTPS/aliases, 200 responses, correct language/RTL, production canonical + hreflang, sitemap, security headers and noindex on verifier/downloads.
6. **Negative-claims review:** EN/AR do not state live EIK, current source truth, real payment release, regulator certification, institutional adoption or signed trademark ownership. A CI-green static link does not establish user value.
7. **Rollback:** preserve the last verified Vercel production deployment and the archived v1 homepage; rollback only if explicitly authorized, not as a side-effect of documentation maintenance.

## External acceptance remains open
Ask an unfamiliar developer or coding agent to reproduce [the EIK example](https://github.com/hamadalmunyif/paygod-kernel-mvp/tree/main/examples/eik-github-actions) without project-author assistance; test an authorized genuine scanner report; compare with GitHub-native controls and direct CLI; obtain a genuinely independently recorded recipient review. These activities are **not** completed by publishing a bilingual page.
