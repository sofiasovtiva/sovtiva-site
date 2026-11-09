# SOVTIVA website quality audit — 2026-11-08

Status: **staged in `audit/website-quality-20261108`; not published**.

## Scope and baseline

- 39 canonical HTML pages, including Journal, Research, Solutions, Partners, AI review, clinic landing page, and articles.
- Read-only checks: source navigation, image references, JSON-LD, canonical URLs, title/description metadata, hreflang availability, RSS/sitemap XML, consent implementation, and visible desktop flows.
- Browser verification: public home + bilingual Journal; local preview home, Journal, language switching, consent panel, and AI review form fields. No real form submission was made.
- No Lighthouse, Core Web Vitals field data, Search Console indexing state, or actual GA4 destination account access was available. Do not claim measured ranking or speed gains.

## Changes staged

| Area | Observed problem | Implemented correction | Verification |
| --- | --- | --- | --- |
| Campaign attribution | `page_location` removed every query parameter and `page_referrer` was forced blank, obscuring referrals and campaign sources after consent | Keep UTM and `from` campaign parameters, drop other queries, sanitize referrer to origin/path, retain explicit analytics opt-in | `node scripts/test-analytics.cjs` PASS |
| Social sharing | Twelve pages lacked a social preview image | Create seven original editorial 1200x630 designs; assign relevant images to home, services, partners, review, clinics, Journal and ventures | All 39 pages now have valid local `og:image` targets |
| Search entity identity | Organization schema lacked a representative logo | Generate 512px logo from existing brand icon and add `logo` to Organization structured data | JSON-LD parse PASS; image exists |
| Sitemap | `/clinicas/` was omitted | Include canonical clinic landing page | Complete 39/39 coverage |
| Jean Phil media | Original inline illustration was ~2.5 MB; declared intrinsic ratio was inaccurate | Serve optimized ~99 KB WebP for inline and preview images, correct dimensions; keep PNG for social meta | Both targets exist, ~96% file-size reduction |
| Journal image load | Five lower article cards had `loading=eager` | Switch to lazy loading and async decode | Source and browser preview checked |
| Keyboard access | Journal index lacked skip link | Add keyboard-only skip-to-content link and main target | Accessible link appears in local preview |
| Spanish editorial | Journal hero and new research cards had awkward or untranslated copy | Hand-review and override prominent Journal headlines, summaries and CTAs | EN/ES toggle inspected in local preview |
| Consent language | Consent notice stayed in its initial language after visitor changed language | Update panel on language-change event and detach listener on dismissal | EN/ES switch tested in local preview |

## Release checklist

- `python scripts/audit-site.py` — PASS, all 39 pages, assets, internal links and sections, schema and sitemap.
- `node scripts/test-analytics.cjs` — PASS, declined consent sends nothing; accepted consent preserves limited campaign/referrer data.
- `node --check assets/analytics.js` and `node --check assets/i18n.js` — syntax PASS.
- Original share-card outputs visually reviewed at 1200x630. Generated files are compact (~28–32 KB each).
- Live site **must not** be changed until the CEO provides explicit publication approval. When approved, refresh and merge against the newest GitHub main to preserve concurrent editorial changes, deploy, and verify the actual live URLs.

## Next work, prioritized by likely value

1. **Native, indexable Spanish service routes**: the client-side language switch makes the experience bilingual but does not create separate, indexable ES versions of most high-intent offers. Create `/es/` service pages with reciprocal hreflang and localized canonicals after content review. Do not falsely mark JavaScript-only translations as separate indexed alternates.
2. **Measure referral and AI visibility**: after deployment and opt-in consent, validate campaigns in GA4 and verify Search Console indexing, impressions, query patterns and conversions. The code patch preserves attribution but cannot retroactively recover erased parameters.
3. **Real device performance**: run mobile Lighthouse / PageSpeed Insights and review Core Web Vitals (LCP, INP, CLS) before asserting numerical improvements; test slow networks and devices.
4. **Form delivery QA**: complete a controlled end-to-end inquiry test only with an approved destination and explicit authorization; confirm Formspree receipt, success/error states and lead attribution.
5. **Editorial cadence + source freshness**: keep entity descriptions, partner relationships, citations and industry advice current. Add new research only when supported by sources and distinct user value.

## Provenance

- Google Search Central, Organization structured data logo guidance: https://developers.google.com/search/docs/appearance/structured-data/organization
- Google Tag Platform, tag setup and parameter reference: https://developers.google.com/tag-platform/gtagjs and https://developers.google.com/tag-platform/gtagjs/reference/parameters
- Web Vitals: https://web.dev/articles/vitals

This audit is an implementation and technical quality report, not a claim of search ranking, lead volume or revenue improvement.
