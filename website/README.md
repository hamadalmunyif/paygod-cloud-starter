# PayGod landing page — review candidate

A complete English, infrastructure-focused landing page with a real local evidence-verification demonstration. A separate Vercel review project is now connected to this branch's repository. Production publication and DNS changes remain pending owner review. See `DEPLOYMENT.md` for the current setup and deployment record.

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

`dist/index.html` is the landing page and sample producer workspace. `dist/verifier/index.html` is a separate recipient workspace that starts empty. `dist/downloads/paygod-verifier.html` is a self-contained downloadable verifier: open it in a desktop browser, disconnect from the network, and choose an exported bundle JSON. Some mobile file preview apps disable JavaScript. No evidence is uploaded, and the verifier does not inherit producer state.

The recipient edition embeds no fixture, calls no producer API, and uses no cookies, local storage, session storage or message-passing for the handoff. Its Content Security Policy blocks network connections and external runtime assets. This demonstrates separate execution of the same browser implementation; it is not an independent third-party audit.

### Try the handoff

1. Open the landing page's sample workspace. The evidence card displays declarations read from the sample files; it is not a verified measurement.
2. Download the bundle and open the separate verifier, which starts with no evidence loaded.
3. Choose the downloaded JSON and run verification. Inspect file integrity, decision binding, and the explicitly unverified source identity and real-world observation.
4. Change the sample measurement or decision, download that bundle, and repeat in the recipient workspace. The relevant check must fail.
5. Download the offline verifier to repeat outside the website. The standalone Python verifier remains the pinned reference implementation.

## Files

- `src/page.html`: authoritative final English page copy and semantic markup.
- `src/style.css`: responsive design, reduced-motion support and focus states.
- `src/verifier.mjs`: browser demonstration verifier.
- `src/sha256.mjs`: local SHA-256 fallback for offline/non-secure-context preview; Web Crypto is preferred when available.
- `src/ui.js`: editable bundle, clean/tampered scenarios, import/export and result lifecycle.
- `src/summary.mjs`: display-only extraction of self-declared evidence-card values; never a source of verification status.
- `src/inspector.html`: shared human-readable workspace and technical inspector.
- `src/standalone.html`: empty recipient workspace and offline verifier shell.
- `PILOT_BRIEF.md`: downloadable template to scope a real source, decision and recipient.
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

Deliverables: self-contained landing page, recipient verifier and offline verifier, plus a pilot brief, all under `dist/`. No Vinext/React runtime is required. A temporary internal preview shell used during review is intentionally excluded from this branch. Keep the static source separate from kernel semantics. No live APIs, CNAME files or secrets are included. `vercel.json` records the review build configuration and skips builds outside Vercel's Preview environment.

Hosting path: GitHub source → static build → separate Vercel review project; retain GoDaddy registration and existing DNS provider. The owner authorized a separate preview. Production deployment and domain changes remain subject to final review. Exact DNS values must be obtained from the chosen hosting project's domain configuration and compared to the existing DNS records before any write. `REVIEW_AR.md` is the original September 28 review; `DEPLOYMENT.md` records subsequent setup.

Preview has `noindex,nofollow`. Remove that only for the approved production release and add its canonical URL. Do not deploy the preview unchanged as an indexed final release.
