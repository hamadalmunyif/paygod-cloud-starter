# PayGod review deployment

## October 2 revision — evidence handoff

The review branch now includes a readable evidence card, a separate empty recipient workspace at `verifier/`, a self-contained downloadable verifier at `downloads/paygod-verifier.html`, and a pilot-scoping brief. Technical JSON and detailed check lists are collapsed initially. Source identity and real-world observation remain visibly unverified.

The verifier core, synthetic fixture, kernel pin and numerical profile are unchanged. Existing browser and upstream Python regression cases passed locally after rebuilding. The three emitted HTML documents passed duplicate-ID, embedded-runtime and JavaScript syntax checks. The recipient outputs contain no sample fixture and block network connections with a Content Security Policy. A new Preview deployment is required for browser handoff verification; the October 1 URL below is the previous design.

Updated: 2026-10-01. This is a review workflow, not a production release approval.

## Source and project

- Repository: `hamadalmunyif/paygod-cloud-starter`
- Review branch: `website/evidence-landing-20260928`
- Original reviewed website commit: `61b143296e3148c6c7a5eb95e9d769a7a02d7c7f`
- Vercel workspace: `paygod1`
- Vercel project: `paygod-evidence-preview`
- Project ID: `prj_AVLxcowK0y5Jn0cbP4p7HckTS3dF`
- Git repository connection confirmed in the Vercel dashboard on October 1.
- The repository's default branch and kernel files are unchanged.

## Reproducible settings

| Setting | Value |
|---|---|
| Root Directory (dashboard) | `website` |
| Include files outside root | Disabled |
| Framework | Other / `null` |
| Build Command | `python3 build.py` |
| Output Directory | `dist` |
| Install Command | Empty; no package installation |
| Allowed build environment | Preview |
| Production branch | `master` (unchanged) |

The project-root `vercel.json` carries the build, output, install and ignore settings. The ignored build command allows Preview (exit 1) and skips other environments (exit 0), as documented at <https://vercel.com/docs/project-configuration/vercel-json#ignorecommand>. Root Directory remains a project dashboard setting.

The HTML and response header request `noindex,nofollow`. This is an indexing preference, not access control. Existing Vercel deployment protection is not disabled by this configuration. No API keys, runtime services or remote evidence processing are required.

## Deployment record

- The first manual request selected this review branch and displayed **Create Preview Deployment**.
- Vercel recorded deployment `6SnwCnrFvAiDK2LXRcBLgBh7Gi2n` as **Production**. The ignored build command returned 0 and canceled it before the build ran.
- That first attempt did not produce a working site.
- The Git-triggered deployment from commit `fd9899d6613b23aea5cbdc53f8a7962db0724b33` completed successfully on October 1: deployment `8bbmQeQiydQwfkSDV1z2c6j2M5jL`, environment **Preview**, status **Ready**, custom-domain assignment **Skipped**.
- Verified preview: <https://paygod-evidence-preview-l18abi5px-paygod1.vercel.app/>
- Deployment details: <https://vercel.com/paygod1/paygod-evidence-preview/8bbmQeQiydQwfkSDV1z2c6j2M5jL>
- Browser checks on the deployed URL: clean bundle **VALID**; altered measurement **INVALID** (`Artifact · measurement.json`); altered receipt verdict **INVALID** (`Decision binding`). The UI was reset to the clean valid sample after verification.
- A fresh local build reproduced the reviewed HTML exactly: SHA-256 `5740a3bcc0ad92431188691e395de5ce49101c326a38b7fc1b0466621b5d0d7f`. The preview-only ignore command was checked under Preview, Production, Development and empty environment values.
- Deployed-page screenshots are saved in `review/paygod-vercel-preview-20261001.jpg` and `review/paygod-vercel-verifier-20261001.jpg`.

Later documentation-only commits may trigger another Preview from the same unchanged website source. The verified URL above identifies the tested deployment specifically.

## Domain remains at GoDaddy

User-provided GoDaddy screenshots from September 30 show GoDaddy Website Builder currently connected to `paygod.net`, nameservers `ns33.domaincontrol.com` and `ns34.domaincontrol.com`, the apex A record labeled `WebsiteBuilder Site`, and `www` pointing to `paygod.net` by CNAME. The dashboard showed a published site last published January 10, 2026. No actual apex IP was exposed in those screenshots.

No GoDaddy setting, nameserver, DNS record or custom-domain association was changed. Domain registration stays at GoDaddy.

Before any production cutover: review the successful preview and verifier results with the owner, approve the final content and production settings, obtain exact destination DNS values from Vercel, preserve unrelated records, and record a rollback plan. The preview's ignore rule and noindex settings must be intentionally reviewed for any approved production release. Do not promote the review build or attach `paygod.net` automatically.
