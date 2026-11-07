// Builds the static website into ./docs (publish with GitHub Pages).
'use strict';
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const out = path.join(root, 'docs');
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });
const cp = (from, to) => fs.copyFileSync(path.join(root, from), path.join(out, to));

for (const f of ['style.css', 'app.js', 'problems-data.js', 'links-data.js']) cp('renderer/' + f, f);
cp('shared/lang.js', 'lang.js');
cp('runner/harness.py', 'harness.py');
cp('web/web-api.js', 'web-api.js');
cp('web/py-worker.js', 'py-worker.js');

// compare.js is a CommonJS module; expose it as window.compareResults
const cmp = fs.readFileSync(path.join(root, 'runner/compare.js'), 'utf8');
fs.writeFileSync(path.join(out, 'compare.js'), '(function(){var module={exports:{}};\n' + cmp + '\nwindow.compareResults=module.exports.compare;})();\n');

// JS worker = shim + the same harness code the desktop app uses
const h = fs.readFileSync(path.join(root, 'runner/harness.js'), 'utf8');
const body = h.slice(h.indexOf('function runAll(dir)'));
const shim = `'use strict';
let INPUT = '', CODE = '';
const process = { stdout: { write: (s) => postMessage({ t: 'out', s }) }, hrtime: { bigint: () => BigInt(Math.floor(performance.now() * 1e6)) } };
const path = { join: (a, b) => a + '/' + b };
const fs = {
  readFileSync: (p) => (String(p).endsWith('input.json') ? INPUT : CODE),
  openSync: () => 1,
  writeSync: (fd, s) => postMessage({ t: 'rec', line: String(s).replace(/\\n$/, '') }),
  closeSync: () => {},
};
const vm = {
  runInThisContext(src, opts) {
    if (!opts) return (0, eval)(src);
    new Function(src); // throws a proper SyntaxError for bad code
    const url = URL.createObjectURL(new Blob([src + '\\n//# sourceURL=solution.js'], { type: 'text/javascript' }));
    try { importScripts(url); } finally { URL.revokeObjectURL(url); }
  },
};
onmessage = (e) => {
  INPUT = e.data.input; CODE = e.data.code;
  try { runAll('/'); } catch (err) { postMessage({ t: 'rec', line: JSON.stringify({ fatal: String(err && err.stack || err).split('\\n').slice(0, 4).join('\\n') }) }); }
  postMessage({ t: 'done' });
};
`;
fs.writeFileSync(path.join(out, 'js-worker.js'), shim + '\n' + body);

// index.html for the browser
let html = fs.readFileSync(path.join(root, 'renderer/index.html'), 'utf8');
html = html.replace('<script src="../shared/lang.js"></script>', '<script src="lang.js"></script>\n  <script src="compare.js"></script>\n  <script src="web-api.js"></script>');
fs.writeFileSync(path.join(out, 'index.html'), html);
fs.writeFileSync(path.join(out, '.nojekyll'), '');
console.log('Built website in', out);
