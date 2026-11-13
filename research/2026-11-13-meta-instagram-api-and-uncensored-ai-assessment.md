# SOVTIVA / Meta Instagram API + local AI / technical research, 2026-11-13

User sources: two user-provided screenshots, one from @sebaslopezinnova advocating Meta's official Instagram API and one thumbnail for Jack Roberts' "I Tested Uncensored AI... It Should Probably Be Illegal…" (2026-11-07, https://www.youtube.com/watch?v=bc7QaDmLmoA). The screenshots alone do not prove credentials, account permissions, installed projects, benchmarks or full video procedure. No screenshots/assets were reproduced. No token-like text copied.

## Published originals
- https://sovtiva.com/journal/instagram-api-meta-oficial-automatizacion-segura-2026/
- https://sovtiva.com/journal/uncensored-ai-local-vs-cloud-agents-reverse-engineering-2026/

## Internal assessment (decision, not implementation)
Meta API: legitimate route for professional accounts to publish media and, within granted scopes, manage comments and user-initiated messages. Instagram Login and Facebook Login differ; app review/advanced access and platform messaging rules apply. Preserve OAuth tokens as secrets, no scraper/password bot. Existing Metricool already handles publication, so custom Meta API integration must NOT become active without a demonstrated inbound-comment/DM review capability gap. Proposed first test is 100% synthetic records, human decision required; no tokens, actual DMs or new Meta App.

Uncensored AI: Model refusal changes ≠ privacy, truthfulness or legitimacy. Jack Roberts describes external API + models, local Ollama + Qwen, and hosted VPS + Tailscale. The USD 0.63/0.32/0.55 sample costs are claims from a video description, not production TCO.

Repos verified (official source, license, fit):
- https://github.com/ollama/ollama | MIT. RESEARCHED / DEFERRED until measured local privacy/latency/cost use-case. Check compute resource and compatibility, especially Windows ARM not having all acceleration backends. Run synthetic isolated data, no paid cloud models.
- https://github.com/deepseek-ai/deepseek-harness | MIT; experimental developer preview; official safety note explicitly says not audited/security not production-ready and may execute model-generated code with file/process/network access. RESEARCHED / DO NOT ADOPT for current production. Existing ChatGPT + review pipeline safer; no demonstrated advantage.
- https://github.com/morluto/rea | MIT; reverse-engineering for lawful software owned or authorized. High attack and compliance surface; not justified over documentation/UI research for Sovtiva SaaS. RESEARCHED / DEFERRED unless an authorized, bounded interoperability/debugging problem arises; no copying third-party code/assets or access bypass.
- https://github.com/tailscale/tailscale | VPN access and policy useful only if we have a server requiring authenticated remote admin. Without server pilot it adds unnecessary system complexity. DEFERRED, not new active.
- Instagram Graph API: provider capability, not a GitHub project. Existing Metricool already scheduled publishing. Do not create competing queue or program.

## Next exact tasks
1. Audit current Instagram inbound workflow capability inside existing authorized platform and whether there is any measurable missing capability. If none, stop. If yes, design least-privilege API pilot with fake events and human approval.
2. Define an original synthetic privacy evaluation dataset and local versus existing workflow acceptance metrics before considering Ollama. No model installation yet.
3. Retain P0 changedetection.io → Crawl4AI → Activepieces local-piloted private review chain and existing P1 Impeccable and HyperFrames pilots; do not replace with a new agent runtime.
4. Before any SaaS reproduction, select a feature based on published lawful behavior, specify original requirements, validate access/licensing and avoid proprietary code or media copying.
5. Check web live deployment and Drive canonical record readback; do not equate source commit with verified live publication.

No third-party subscriptions, new app connections, raw credentials, customer records, paid credits, unsolicited DM/outreach, social posts, new Drive folders or new active OSS projects.
