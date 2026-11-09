const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const code = fs.readFileSync(require('node:path').join(__dirname, '..', 'assets/analytics.js'), 'utf8');

function run(choice, href, referrer) {
  const loaded = [];
  const location = new URL(href);
  const document = {
    documentElement: { lang: 'en' },
    readyState: 'complete',
    title: 'sovtiva test',
    referrer,
    head: { appendChild: item => loaded.push(item) },
    createElement: tagName => ({ tagName })
  };
  const localStorage = { getItem: () => choice };
  const window = { location, localStorage };
  vm.runInNewContext(code, { window, document, localStorage, URL, Set, Date });
  return { window, loaded };
}

const declined = run('no', 'https://sovtiva.com/?utm_source=reddit', 'https://reddit.com/r/business/');
assert.equal(declined.window.gtag, undefined, 'Declining consent must not load Analytics');
assert.equal(declined.loaded.length, 0, 'Declining consent must not inject scripts');

const accepted = run('yes', 'https://sovtiva.com/ai-review/?utm_source=chatgpt&utm_medium=referral&email=private@example.com#form', 'https://www.reddit.com/r/smallbusiness/?secret=1');
const config = [...accepted.window.dataLayer].find(args => args[0] === 'config')[2];
assert.equal(config.page_location, 'https://sovtiva.com/ai-review/?utm_source=chatgpt&utm_medium=referral');
assert.equal(config.page_referrer, 'https://www.reddit.com/r/smallbusiness/');
assert.equal(accepted.loaded.length, 1, 'Consent should inject one Google tag');
assert.ok(accepted.loaded[0].src.startsWith('https://www.googletagmanager.com/gtag/js?id='));

console.log('Analytics consent, UTM attribution and referrer privacy: PASS');
