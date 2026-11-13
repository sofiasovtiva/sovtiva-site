# SOVTIVA Editorial Edition 04 — source-led design implementation
Date: 2026-11-13
Source articles: https://sovtiva.com/journal/award-winning-websites-editorial-navigation-sovtiva-2026/ and https://sovtiva.com/journal/award-winning-websites-editorial-navigation-sovtiva-2026/es/

## Observed issue
Existing assets/research-v2.css, journal/styles.css and assets/site.css used dense sans headlines, weights around 800-900, compressed tracking. The site was functional but long research pieces felt too heavy.

## Independent award references, not borrowed assets
- The Webby Awards 2026, Best User Experience: https://winners.webbyawards.com/winners/websites-and-mobile-sites/features-design/best-user-experience
- The Webby Awards 2026, Best User Interface: https://winners.webbyawards.com/winners/websites-and-mobile-sites/features-design/best-user-interface
- The Webby Awards 2026, Best Visual Design – Aesthetic: https://winners.webbyawards.com/winners/websites-and-mobile-sites/features-design/best-visual-design-aesthetic
- The Webby Awards 2026, Best Practices: https://winners.webbyawards.com/winners/websites-and-mobile-sites/features-design/best-practices
- The Webby Awards 2026, Best Homepage and Editorial Feature: https://winners.webbyawards.com/winners/websites-and-mobile-sites
- CSS Design Awards 2025 Website of the Year winners (announced February 2026): https://www.cssdesignawards.com/blog/2025-website-of-the-year-winners/430/
- The Webby Awards 2026, Best Trend/Insights/Impact Report: https://winners.webbyawards.com/winners/websites-and-mobile-sites/features-design/best-trend-insights-or-impact-report
- W3C, WCAG 2.2 Animation from Interactions: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions
- web.dev, Interaction to Next Paint: https://web.dev/articles/optimize-inp
2026 Webby: Pentagram Archive UX, DICH Fashion UI, Igloo Inc visual aesthetics, Docusign Best Practices, The Renaissance Edition homepage and Pinterest Predicts 2026 report. 2025 CSS Design Awards (Feb 2026): Dropbox Brand Website of the Year; Exat Typeface Best UI. Awards establish recognition, not proven performance metrics or conversion impact.

## Exact source changes
- assets/research-v2.css: typography Instrument Serif 400 for titles and major article headings, DM Sans for body, lighter emphasis, calmer letter spacing, accessible hover and focus states, optional CSS scroll progress.
- journal/styles.css: calmer serif display and card headlines, offwhite editorial cards, CSS styles for reading-room search and category filters.
- journal/index.html + assets/journal-discovery-v4.js: a progressive enhancement across the four existing sections (Latest, Field guides, AI & systems, Partner desk), live local text search, article count, empty state and Surprise me. No network request, API, analytics additions or customer data.
- index.html + assets/site.css: soften display headlines; retain the headline "What brings you here?", the four intent routes, existing bilingual controls and workflow lab; add three optional research-path cards (native swipe on mobile).
- original article EN/ES with canonical, hreflang, BlogPosting JSON-LD, sources; Journal entry, sitemap and RSS.
- No images generated; no vendor logos/assets copied, no JS framework, no paid plugins, no backend service.

## Critical constraints and test plan
- Semantic links/buttons, visible focus, W3C reduced-motion; input is hidden until script loads. Disabling JS preserves all Journal content.
- Confirm that article headings use normal serif weight and not 800px billboard blocks at phone widths 375, 768, 1280.
- Test instant search with matching/empty queries, Escape clear, every filter, random destination and keyboard Tab/Enter; verify contents restored after switching filters.
- Test homepage four intent choices, original flow lab, AI review and EN/ES routes unaffected.
- Verify actual phone browser, VoiceOver/keyboard, wrapping, long Spanish headlines, fonts fallback, CLS, LCP and INP with real evidence before declaring quality/performance gains. Google good INP at p75 <= 200ms is a TARGET, not measured result.
- Maintain product/service honesty; no invented clients, awards, revenue, or proof.
- GitHub Pages and IndexNow readback validate deployment workflow, not independently prove real-browser rendering, indexing or traffic.
- No new Drive folders, new OSS installations, spending or outbound.

## Next single task
Inspect actual mobile and desktop renders (Safari iPhone and desktop), especially mobile header, search and EN/ES home discovery; fix any overflow, then baseline Web Vitals and real qualified click-through before adding more motion.
