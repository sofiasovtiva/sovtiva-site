/* Deterministic original editorial share cards. Run: node scripts/create-share-cards.cjs */
const sharp = require('sharp');
const fs = require('node:fs');
const path = require('node:path');

const root = path.join(__dirname, '..', 'assets', 'share');
fs.mkdirSync(root, { recursive: true });

const cards = [
  {file: 'sovtiva-studio.png', tag: 'THE SOVTIVA COLLECTIVE / 01', lines: ['What brings', 'you here?'], bg: '#0b1923', ink: '#edf4ef', accent: '#bfe6f0', second: '#223e4c', marker: '01'},
  {file: 'sovtiva-journal.png', tag: 'RESEARCH · FIELD NOTES / 02', lines: ['Ideas worth', 'sharing.'], bg: '#e9f1ee', ink: '#102b38', accent: '#722f47', second: '#cee1df', marker: '02'},
  {file: 'sovtiva-partners.png', tag: 'INDEPENDENT SPECIALISTS / 03', lines: ['The right', 'connection.'], bg: '#f3eadb', ink: '#273329', accent: '#702e44', second: '#d6cab8', marker: '03'},
  {file: 'sovtiva-ai-systems.png', tag: 'AI · AUTOMATION · WORKFLOWS / 04', lines: ['Less manual', 'work.'], bg: '#183443', ink: '#edf3f0', accent: '#c0e7ee', second: '#345c62', marker: '04'},
  {file: 'sovtiva-ai-review.png', tag: 'FREE FIRST LOOK / 05', lines: ['One task.', 'A better way.'], bg: '#6c2d43', ink: '#fff4ea', accent: '#c2e7ee', second: '#8c4d5e', marker: '05'},
  {file: 'sovtiva-clinicas.png', tag: 'CONSULTORIOS · CLÍNICAS / 06', lines: ['Menos pasos.', 'Más atención.'], bg: '#d0e8e9', ink: '#152c37', accent: '#702e44', second: '#eaf2ec', marker: '06'},
  {file: 'sovtiva-world.png', tag: 'BOOKS · TOOLS · ORIGINAL MEDIA / 07', lines: ['One name.', 'Many ideas.'], bg: '#dcd8bd', ink: '#22332a', accent: '#702e44', second: '#c5cead', marker: '07'}
];

const escape = value => value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

async function writeCard(card) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
    <defs><pattern id="grid" width="39" height="39" patternUnits="userSpaceOnUse"><path d="M39 0H0V39" fill="none" stroke="${card.ink}" stroke-opacity=".09" stroke-width="1"/></pattern></defs>
    <rect width="1200" height="630" fill="${card.bg}"/>
    <rect width="1200" height="630" fill="url(#grid)"/>
    <circle cx="1065" cy="220" r="236" fill="none" stroke="${card.accent}" stroke-opacity=".55" stroke-width="2"/>
    <circle cx="1065" cy="220" r="155" fill="${card.second}" fill-opacity=".65" stroke="${card.accent}" stroke-opacity=".5" stroke-width="2"/>
    <circle cx="1065" cy="220" r="65" fill="none" stroke="${card.accent}" stroke-width="4"/>
    <path d="M845 500L1190 155M895 520L1190 225" stroke="${card.accent}" stroke-opacity=".8" stroke-width="3"/>
    <rect x="75" y="68" width="45" height="6" rx="3" fill="${card.accent}" transform="rotate(-18 75 68)"/>
    <rect x="90" y="83" width="32" height="6" rx="3" fill="${card.accent}" transform="rotate(-18 90 83)"/>
    <text x="145" y="89" font-family="DejaVu Sans,Arial,sans-serif" font-weight="bold" font-size="37" letter-spacing="-2" fill="${card.ink}">sovtiva.</text>
    <text x="76" y="179" font-family="DejaVu Sans,Arial,sans-serif" font-size="19" font-weight="bold" letter-spacing="3.3" fill="${card.accent}">${escape(card.tag)}</text>
    <text x="70" y="306" font-family="DejaVu Sans,Arial,sans-serif" font-size="83" font-weight="bold" letter-spacing="-4" fill="${card.ink}">${escape(card.lines[0])}</text>
    <text x="70" y="405" font-family="DejaVu Sans,Arial,sans-serif" font-size="83" font-weight="bold" letter-spacing="-4" fill="${card.ink}">${escape(card.lines[1])}</text>
    <path d="M76 484H740" stroke="${card.accent}" stroke-width="3"/>
    <text x="76" y="557" font-family="DejaVu Sans,Arial,sans-serif" font-size="20" letter-spacing="2" fill="${card.ink}" opacity=".82">SOVTIVA.COM</text>
    <text x="1109" y="557" text-anchor="end" font-family="DejaVu Sans,Arial,sans-serif" font-size="20" font-weight="bold" letter-spacing="1" fill="${card.ink}" opacity=".85">S//26 · ${card.marker}</text>
  </svg>`;
  await sharp(Buffer.from(svg)).png({ compressionLevel: 9, palette: true, effort: 8 }).toFile(path.join(root, card.file));
}

Promise.all(cards.map(writeCard)).then(() => console.log(`Rendered ${cards.length} original 1200×630 share cards`)).catch(error => { console.error(error); process.exitCode = 1; });
