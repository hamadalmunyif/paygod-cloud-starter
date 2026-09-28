# PayGod landing page — review candidate

A complete English, infrastructure-focused landing page with a real local evidence-verification demonstration. No deployment has been configured or performed. No production domain or DNS changes are included.

## Run

Python 3.10+ and Node 22+ are sufficient for the build and tests. No npm install, API credentials, database, remote fonts or CDN JavaScript is needed.

```bash
cd website
python3 build.py
python3 -m http.server 8080 --directory dist
# Open http://localhost:8080
node tests/verify.mjs
python3 tests/upstream.py
python3 vendor/verify_portable_evidence.py demo/bundle --result demo/local-result.json
```

PowerShell:

```powershell
Set-Location website
python build.py
python -m http.server 8080 --directory dist
# Open http://localhost:8080
node tests/verify.mjs
python tests/upstream.py
python vendor/verify_portable_evidence.py demo/bundle --result demo/local-result.json
```

`dist/index.html` is the complete self-contained preview. It can also be opened directly in a desktop browser. Some mobile file previews disable JavaScript; a normal browser on a local server or future HTTPS preview is required in that case. There is no remote processing of imported evidence.

## Files

- `src/page.html`: authoritative final English page copy and semantic markup.
- `src/style.css`: responsive design, reduced-motion support and focus states.
- `src/verifier.mjs`: browser demonstration verifier.
- `src/sha256.mjs`: local SHA-256 fallback for offline/non-secure-context preview; Web Crypto is preferred when available.
- `src/ui.js`: editable bundle, clean/tampered scenarios, import/export and result lifecycle.
- `demo/sample.json`: UTF-8 transport wrapper around a synthetic compatible bundle.
- `demo/bundle/`: unwrapped artifacts accepted by the pinned upstream verifier.
- `demo/generate.py`: reproducible synthetic fixture generator; not a kernel execution or domain pack.
- `vendor/verify_portable_evidence.py`: unchanged upstream v0.2.0, Apache-2.0, pinned to kernel commit `f405fdf7cabebddda62196299e50b0598e3e663b`.
- `REVIEW_AR.md`: current-state review, design, architecture, release proposal and outstanding access limits.
- `COPY_EN.md`: extracted final reader-facing copy.

## Demonstration boundary

The browser verifier checks manifest/receipt kind and version, file SHA-256 and size, manifest binding, aggregate digest, locked ledger presence, ledger chain, decision/pack/input bindings and injected-clock consistency. It does not execute a pack, authenticate an issuer, verify real-world facts or authorize a downstream action.

This is **not** a production verifier distribution or a signed trust root. The UI visibly labels it a demo. It intentionally implements a restricted safe-integer numeric profile and stricter file-name limits. JSON duplicate keys are parsed with the platform's normal last-value semantics; hostile-input production hardening requires a strict parser and a separately audited full-profile implementation. The JS fallback is tested against Node SHA-256 but has not been independently audited. JavaScript Date parsing is not claimed to have full Python timestamp-profile parity. The upstream Python implementation remains the reference.

A malicious producer can generate an entirely new self-consistent bundle. Integrity checking alone does not establish provenance, freshness or a genuine observation. `generated_at` is an injected value bound to the evidence, not a trusted timestamp. The displayed digest is calculated from manifest file commitments; individual file checks determine whether actual bytes meet them. Never use this demo as an authorization decision.

The example pack digest is a synthetic identifier, not a published/verified executable pack. The sample illustrates a `flag` result for 420 kWh against a fictional 400 kWh threshold; it is not an environmental compliance rule or a real measurement.

## Architecture and deployment

Production deliverable: static HTML + CSS + browser JS, all in `dist/index.html`. No Vinext/React runtime is required. A temporary internal preview shell used during review is intentionally excluded from this branch. Keep the static source separate from kernel semantics. No workflows, live APIs, CNAME files, hosting bindings, secrets or automatic publishing are added.

Recommended future hosting: GitHub source → reviewed static build → Vercel project; retain GoDaddy registration and existing DNS provider. Deployments and domain changes remain subject to owner approval. Exact DNS values must be obtained from the chosen hosting project's domain configuration and compared to a real exported DNS zone before any write. See `REVIEW_AR.md`.

Preview has `noindex,nofollow`. Remove that only for the approved production release and add its canonical URL. Do not deploy the preview unchanged as an indexed final release.
