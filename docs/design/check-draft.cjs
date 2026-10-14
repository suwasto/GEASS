// Static design checks only; this does not launch a browser or verify rendered interaction.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, 'preview.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
new Function(script);
const fixtures = vm.runInNewContext(script.slice(0, script.indexOf('const $')) + '\npackages');
assert.equal(fixtures.length, 6);
assert.equal(new Set(fixtures.map(p => p.id)).size, fixtures.length);
assert(fixtures.every(p => p.id.startsWith('DEMO-') && Number.isSafeInteger(p.amount) && p.amount > 0));
assert.equal(fixtures.filter(p => p.state === 'supported').length, 3);
assert.equal(fixtures.filter(p => p.state === 'insufficient').length, 2);
assert.equal(fixtures.filter(p => p.state === 'normal').length, 1);
assert(!fixtures.some(p => p.id === 'DEMO-RUP-007'), 'Private reviewer draft must not enter radar fixtures');
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
assert.equal(new Set(ids).size, ids.length, 'Duplicate element identifiers');
for (const match of html.matchAll(/\bfor="([^"]+)"/g)) assert(ids.includes(match[1]), 'Unbound label: ' + match[1]);
for (const match of script.matchAll(/\$\('([^']+)'\)/g)) assert(ids.includes(match[1]), 'Missing element: ' + match[1]);
assert(!/<(?:script|link)[^>]+(?:src|href)=|fetch\(|XMLHttpRequest|https?:\/\//i.test(html), 'Draft must remain offline');
assert(html.includes('DATA SINTETIS') && html.includes('prefers-reduced-motion') && html.includes('<dialog'));
function luminance(hex) {
  const rgb = hex.match(/[a-f\d]{2}/gi).map(v => parseInt(v, 16) / 255).map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
  return rgb[0] * .2126 + rgb[1] * .7152 + rgb[2] * .0722;
}
for (const [label, fg, bg] of [['body', '#edf2f7', '#121e2d'], ['muted', '#b2c0ce', '#121e2d'], ['quiet', '#93a7bc', '#192838'], ['amber', '#f4c16b', '#30291f'], ['mint', '#93d5bc', '#19312d'], ['error', '#ffb5ac', '#38262a'], ['primary button', '#15202d', '#f4c16b']]) {
  const values = [luminance(fg), luminance(bg)].sort((a,b) => b-a);
  const ratio = (values[0] + .05) / (values[1] + .05);
  assert(ratio >= 4.5, label + ' text contrast below 4.5:1');
  console.log(label + ' contrast: ' + ratio.toFixed(2) + ':1');
}
console.log('PASS: JavaScript syntax, six synthetic fixtures, role separation, IDs/labels, offline policy and token contrast.');
