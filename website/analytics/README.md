# PayGod.net privacy-first analytics contract (STAGING PLAN — NOT ENABLED)

Status: PROPOSED / DOCUMENTATION AND TEST PLAN ONLY, 2026-10-16. This directory does **not** install the PostHog SDK, transmit events, turn on session replay or authorize a production deploy.

## Observed facts / scope

- PayGod's connected PostHog app returned an active newly created **Default project** on 2026-10-16. The event schema showed **no events observed in the last 30 days**. Connection to the ChatGPT app is **not** proof that paygod.net is instrumented or consent has been obtained.
- Current production website source: `website/paygod-production@9d3ae02356cc510af08e8e442eb5f6a01f5a8ae9` (re-pin at candidate PR).
- This plan is about website/product experience, **not** proof of a financial release, source authenticity, scanner status or Kernel correctness.

## Intended observable questions

1. Can a first-time developer find the canonical EIK example and identify the limit of `allow`?
2. Which bounded lab screen is most confusing? Does the user distinguish a *policy expectation* from executing Kernel, and integrity from source truth?
3. Is the independent verifier path discoverable and usable without producer assistance?
4. Which requests for integrations recur, without transmitting partner documents or sensitive evidence?

## Event taxonomy

Machine-checkable candidate in [EVENTS.v0.json](EVENTS.v0.json); all custom events namespaced `pg_`. Events not tied to a real action **must not** be emitted. `pg_integration_interest_submitted` is reserved, not active until an explicit feedback experience and valid consent exist.

Property scope should be allowlisted only:
`route_id, page_locale, site_release, surface, challenge_kind, integrity_result, issuer_authenticity, target_kind, deployment_env`.
For completion tracking, use only an anonymous session-local random correlation ID if essential and separately reviewed; by default no unique identity is required.

**Prohibited**: uploaded raw bundles and file contents, decision/receipt hashes, fingerprints or key identifiers, authentic scanner finding details, CVE IDs, customer/personal data, tool arguments/prompts, credentials, tokens, industrial readings, emails/phone numbers, raw URLs/query params, unredacted session replay, unrestricted auto-capture. Analytics **never becomes evidence of Kernel execution or external source truth**.

## Suggested controlled rollout (separate future PRs)

0. Confirm which PostHog **organization/project**, hosting region, retention policy, and consent/legal basis should receive paygod.net events; rename/segregate product project if required. Do not put service secrets in the static frontend. A public website capture key is not a production secret but must be project-scoped and reviewed.
1. Build Preview-only instrumentation behind an explicit `ANALYTICS_ENABLED` build configuration **off by default**. Autocapture/session replay/person identification all disabled by default; allowlist events only. Do not send requests for `/verifier/` evidence content or user-selected files.
2. Check CSP/connect-src changes and latency; load analytics only on permitted pages, verify no external requests when disabled, and test consent behavior before enabling on the public domain.
3. Exercise one controlled test for each allowed event on Vercel Preview; verify exact event names/fields within the target PostHog project, and discard/test-filter fake data.
4. Use native PostHog metrics with verified event definitions and correct project timezone; do not invent funnels from absent events. Separately show `UNKNOWN` when traffic is insufficient.
5. Production: a **separately owner-approved** versioned website PR, verified Vercel deployment commit/alias, region/privacy review and rollback route. No auto-promotion from this documentation PR.

## Comparison / success

Measure documented EIK guide discovery, lab completion and verified independent offline handoff against a non-analytics control period; exclude bots, self-tests and preview. Distinguish click telemetry from actual verified code execution and from commercial acceptance. Do not claim product-market fit from pageviews.

See [site release rules](../EIK_SITE_RELEASE_2026-10-14.md), [canonical Kernel claims](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/docs/CLAIMS_REGISTER.md), and [Kernel verifier parity issue #74](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/74).
