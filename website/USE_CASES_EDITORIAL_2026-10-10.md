# PayGod Website — Architecture and Pack Use Cases (2026-10-10)

Status: **BILINGUAL EDITORIAL ADDITION / DRAFT / NOT A NEW EXECUTION PRODUCT**

## Current intent

The website explains **why one canonical Kernel can be useful in multiple domains**. It is not announcing a Pack marketplace, institutional accreditation, operating SaaS, paid community submission program, or royalty-sharing system.

The public technical source is exclusively [paygod-kernel-mvp](https://github.com/hamadalmunyif/paygod-kernel-mvp). No other repository is presented as a shipped PayGod technical asset.

## How to read the pages

- English: `/use-cases/`
- Arabic RTL: `/ar/use-cases/`
- Discoverability: links in the original landing and the existing `/explore/` / `/ar/` evidence atlas.
- Step 1: external source (not automatically trusted).
- Step 2: pre-Kernel evidence admission (workflow responsibility, **not** an automatically enforced Kernel runtime condition on all entrypoints).
- Step 3: canonical Kernel Pack evaluation and scoped rule result.
- Step 4: portable bundle and independent integrity verification (a separate conceptual workflow demonstration).
- Step 5: recipient's own reliance/authorization (not decided by the Kernel).

## Packs and what is real

| Pack | Canonical source | Source-controlled policy cases | Publicly claimed maturity |
|---|---|---:|---|
| GHG Scope 1 & 2 | [pack.yaml](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/packs/core/ghg-scope-1-2-guard/pack.yaml) · [cases.yaml](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/packs/core/ghg-scope-1-2-guard/tests/cases.yaml) | 3 | Executable Pack; synthetic policy fixtures; **not** emissions calculation or certified source truth |
| Critical CVE | [pack.yaml](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/packs/core/critical-cve-blocker/pack.yaml) · [cases.yaml](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/packs/core/critical-cve-blocker/tests/cases.yaml) | 3 | Executable Pack; synthetic policy fixtures; **not** scanner or production release enforcement |
| ISO 27001 Policy Review | [pack.yaml](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/packs/core/iso27001-policy-review/pack.yaml) · [cases.yaml](https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/packs/core/iso27001-policy-review/tests/cases.yaml) | 4 | Executable Pack; four fixtures, **three illustrative outcomes** featured; **not** ISO certification |

Note: The page illustrates **three** state examples per Pack. ISO has **four** source-controlled fixtures; its additional DENY (overdue review) remains accessible by linking to the source tests, and is not erased or described as absent.

Fixture results are authored from the Pack's declared test cases. They are **not browser-side pack execution** and are not fresh independent measurements. The website builder does not invoke the .NET policy engine to recompute these examples.

## Boundaries required in visible copy

- A clean/internally valid bundle does not prove a true measurement, an authenticated scanner, authorized ISO sign-off or a binding audit finding.
- A matching receipt signature does not establish regulator authorization.
- The user is not asked to upload real enterprise data.
- The current generic Kernel `run` path does not automatically validate every Pack's embedded `spec.inputs.schema`.
- [Kernel PR #103](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/103) is draft research with a GHG shape-only candidate; it is not a merged production gate and **must not be linked as a second shipped source**.
- Links on the two pages point only to the public canonical Kernel repository and existing site routes.

## Future pack contributors (NOT THIS PHASE)

A potential future contribution program may let outside authors submit Packs, subject to independent tests, explicit acceptance governance and rights/benefit terms. **None of its conditions, submission endpoints, certification marks, prices, royalties, reward shares or author benefits has been approved.** Do not publish an intake form or a "Submit Pack" CTA yet. That requires a separately authorized governance design.

## Publication gate

1. Website PR passes builder, existing browser verifier suite, independent Python verifier suite, atlas audit and new bilingual page tests.
2. Review Arabic/English mobile layout, accessibility, copy, links, and absence of inadvertent "production-ready" labels.
3. Verify the example outcomes match the source Pack fixtures at the release revision.
4. Keep existing `/verifier/` and offline-download behavior unchanged.
5. Merge/publication only after approved review. No automated production domain promotion by this editorial PR alone.
