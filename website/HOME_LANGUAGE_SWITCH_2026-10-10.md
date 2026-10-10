# Home language-switch correction — 2026-10-10

**Status:** proposed Arabic editorial homepage and reciprocal homepage locale switch. 

## User-observed bug
The original `/ ` English homepage had a navigation item labelled `العربية` which linked to `/ar/`. But `/ar/` is the Arabic **Evidence Atlas**, not a translated homepage. This was not an actual homepage language switch.

## Correction
- `/ ` — existing English homepage, with a conspicuous `العربية` switch.
- `/ar/home/` — newly translated RTL homepage preserving the English homepage's main sections and synthetic evidence-handoff feature.
- `/ar/` — existing Arabic Evidence Atlas, **unchanged route** to preserve current links.
- `/ar/use-cases/` — existing Arabic Kernel Use Cases, **unchanged route**.
- The English homepage `العربية` selector points to `/ar/home/`. The Arabic homepage English selector returns to `/ `.
- Arabic Atlas and Arabic Use Cases expose links to the new Arabic homepage.
- The standalone verifier `/verifier/` and its external/offline counterparts are not modified.

### Important localization limit
The homepage's explanatory text and navigation are localized in Arabic. Its **existing synthetic interactive demo, underlying browser verifier controls, and dynamic test interface remain in English** for now, clearly disclosed in Arabic before the embedded demo. The demo is the original shared implementation, not a fork or a second verifier. Full Arabic UI localization of the verifier should be its own tested change; the home language switch does **not** silently modify the verifier contract.

## Checks
- Native `lang=ar`, `dir=rtl` and language-specific title/metadata.
- `hreflang=en/ar/x-default` points to corresponding homepages, and production canonical tags match the exact path.
- Local route and fragment checking for English and Arabic homepages.
- Homepage and Case/Atlas navigation lead to same-language contexts.
- Homepage sections are preserved; source code links remain canonical Kernel only.
- Existing verifier and browser-verifier CI tests remain mandatory.
- Sitemap includes `/ar/home/` on production builds only; preview is `noindex`.

## Future governance, not this change
No marketplace, contributor submission process, revenue sharing or institutional Pack certification is announced. This change is website navigation and editorial localization only.
