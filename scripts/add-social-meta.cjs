/* Idempotent metadata insertion for the compactly formatted service pages. */
const fs = require('node:fs');
const path = require('node:path');
const pages = {
  'solutions/index.html': 'sovtiva-studio.png',
  'partners/index.html': 'sovtiva-partners.png',
  'ai-automation-small-business/index.html': 'sovtiva-ai-systems.png',
  'custom-software-ai/index.html': 'sovtiva-ai-systems.png',
  'technology-partner-match/index.html': 'sovtiva-partners.png'
};
for (const [relative, image] of Object.entries(pages)) {
  const file = path.join(__dirname, '..', relative);
  let content = fs.readFileSync(file, 'utf8');
  if (content.includes('property="og:image"')) continue;
  const match = content.match(/<meta property="og:url" content="[^"]+">/);
  if (!match) throw new Error(`No og:url found: ${relative}`);
  content = content.replace(match[0], match[0] + `<meta property="og:image" content="https://sovtiva.com/assets/share/${image}"><meta name="twitter:card" content="summary_large_image">`);
  fs.writeFileSync(file, content);
  console.log(`Added image preview: ${relative}`);
}
