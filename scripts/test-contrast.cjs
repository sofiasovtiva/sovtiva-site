#!/usr/bin/env node
/* Dependency-free contrast regression checks for exact CSS tokens audited in PSI.
 * Browser-based Lighthouse and manual QA remain necessary. */
const fs = require('node:fs');
const path = require('node:path');
const css = {
  site: fs.readFileSync(path.join(__dirname, '../assets/site.css'), 'utf8'),
  review: fs.readFileSync(path.join(__dirname, '../assets/revenue.css'), 'utf8'),
};
const samples = [
  ['site', '.fit-intro p', '#eaf0ed'],
  ['site', '.partner-lead p,.partner-tile p', '#dce8e6'],
  ['site', '.partner-tile-head,.partner-type', '#f0f4f0'],
  ['site', '.partner-note', '#dce8e6'],
  ['site', '.mock-eyebrow,.mock-data,.mock-footer', '#f2f5ee'],
  ['site', '.ventures-intro p', '#f0eee8'],
  ['site', '.ventures-section .eyebrow', '#f0eee8'],
  ['site', '.venture-book span', '#b6c1b8'],
  ['review', '.review-spotlight-actions>span', '#dae8df'],
  ['review', '.review-card-index', '#f3f1e9'],
  ['review', '.review-card>p', '#f3f1e9'],
  ['review', '.review-form-note', '#f3f1e9'],
  ['review', '.review-direct', '#f3f1e9'],
  ['review', '.review-steps .review-eyebrow', '#e9f1ed'],
  ['review', '.review-step p', '#e9f1ed'],
];
function luminance(hex) {
  const value = hex.slice(1);
  const v = [0, 2, 4].map(i => parseInt(value.slice(i, i + 2), 16) / 255)
    .map(n => n <= .04045 ? n / 12.92 : ((n + .055) / 1.055) ** 2.4);
  return .2126 * v[0] + .7152 * v[1] + .0722 * v[2];
}
function lastColor(text, selector) {
  const decls = text.split('}').filter(rule => rule.includes(selector + '{'));
  for (let i = decls.length - 1; i >= 0; i--) {
    const rule = decls[i].split('{').at(-1);
    const match = rule.match(/(?:^|;)\s*color:\s*(#[0-9a-fA-F]{6})\b/);
    if (match) return match[1];
  }
  return null;
}
let failures = 0;
for (const [file, selector, background] of samples) {
  const foreground = lastColor(css[file], selector);
  const [hi, lo] = [foreground ? luminance(foreground) : 0, luminance(background)].sort((a,b) => b-a);
  const ratio = foreground ? (hi + .05) / (lo + .05) : 0;
  const pass = ratio >= 4.5;
  if (!pass) failures++;
  console.log(`${pass ? 'PASS' : 'FAIL'} ${selector}: ${ratio.toFixed(2)}:1`);
}
if (!/\.contact-direct a\{[^}]*text-decoration:underline/.test(css.site)) {
  failures++;
  console.error('FAIL contact link missing underline');
}
if (failures) process.exitCode = 1;
else console.log(`PASS: ${samples.length} color pairs and inline link cue`);
