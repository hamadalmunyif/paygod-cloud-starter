# PayGod review deployment

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
- No successful deployment or working preview URL is claimed by that attempt. The next attempt uses the Git-connected review branch with these committed settings.

## Domain remains at GoDaddy

User-provided GoDaddy screenshots from September 30 show GoDaddy Website Builder currently connected to `paygod.net`, nameservers `ns33.domaincontrol.com` and `ns34.domaincontrol.com`, the apex A record labeled `WebsiteBuilder Site`, and `www` pointing to `paygod.net` by CNAME. The dashboard showed a published site last published January 10, 2026. No actual apex IP was exposed in those screenshots.

No GoDaddy setting, nameserver, DNS record or custom-domain association was changed. Domain registration stays at GoDaddy.

Before any production cutover: review the successful preview and verifier results with the owner, approve the final content and production settings, obtain exact destination DNS values from Vercel, preserve unrelated records, and record a rollback plan. The preview's ignore rule and noindex settings must be intentionally reviewed for any approved production release. Do not promote the review build or attach `paygod.net` automatically.
