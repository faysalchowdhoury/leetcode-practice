// Browser replacement for the Electron preload API: runs JavaScript in a Web Worker and Python in Pyodide (WebAssembly).
(function () {
  'use strict';
  const RUN_TIMEOUT_MS = 10000;
  const PYODIDE_VERSION = '0.26.4';
  const MONACO_BASE = 'https://cdn.jsdelivr.net/npm/monaco-editor@0.52.0/min/vs';

  function slim(p) {
    return { kind: p.kind, fn: p.fn, params: p.params, ret: p.ret, inplace: p.inplace, design: p.design, rt: p.rt, post: p.post };
  }
  function trunc(s, n) { s = String(s == null ? '' : s); return s.length > n ? s.slice(0, n) + '\n... (output truncated)' : s; }

  // Same result processing as runner/runner.js
  function finish(p, tests, recs, fatal, stdout, timedOut, crashMsg) {
    const result = { status: 'Accepted', cases: [], stdout: trunc(stdout, 6000), message: '', passed: 0, total: tests.length, maxMs: 0 };
    if (fatal) {
      result.status = fatal.syntax ? 'Compile Error' : 'Runtime Error';
      result.message = fatal.fatal;
      result.cases = tests.map((t, i) => ({ index: i, status: 'skipped' }));
      return result;
    }
    let firstMissing = true;
    for (let i = 0; i < tests.length; i++) {
      const t = tests[i];
      const rec = recs[i];
      let c;
      if (!rec) {
        if (timedOut) c = { index: i, status: firstMissing ? 'tle' : 'skipped' };
        else if (firstMissing) c = { index: i, status: 'error', message: crashMsg || 'The program stopped before producing a result.' };
        else c = { index: i, status: 'skipped' };
        firstMissing = false;
      } else if (!rec.ok) {
        c = { index: i, status: 'error', message: rec.err };
      } else {
        const ok = window.compareResults(p.cmp || 'exact', rec.out, t.expected, p.kind === 'func' ? t.in : null);
        c = { index: i, status: ok ? 'pass' : 'fail', actual: rec.out, ms: rec.ms };
        if (ok) result.passed++;
        if (typeof rec.ms === 'number') result.maxMs = Math.max(result.maxMs, rec.ms);
      }
      result.cases.push(c);
    }
    const has = (s) => result.cases.some((c) => c.status === s);
    if (has('error')) { result.status = 'Runtime Error'; result.message = result.cases.find((c) => c.status === 'error').message; }
    else if (has('tle')) result.status = 'Time Limit Exceeded';
    else if (has('fail')) result.status = 'Wrong Answer';
    return result;
  }

  function runJs(code, p, tests) {
    return new Promise((resolve) => {
      const w = new Worker('js-worker.js');
      const recs = {}; let fatal = null; let out = ''; let done = false; let timedOut = false; let crash = '';
      const end = () => { if (done) return; done = true; clearTimeout(timer); w.terminate(); resolve(finish(p, tests, recs, fatal, out, timedOut, crash)); };
      const timer = setTimeout(() => { timedOut = true; end(); }, RUN_TIMEOUT_MS);
      w.onmessage = (e) => {
        const m = e.data;
        if (m.t === 'rec') { try { const r = JSON.parse(m.line); if (r.fatal) fatal = r; else recs[r.i] = r; } catch (_) {} }
        else if (m.t === 'out') out += m.s;
        else if (m.t === 'done') end();
      };
      w.onerror = (e) => { crash = String(e.message || 'The program crashed.'); end(); };
      w.postMessage({ code, input: JSON.stringify({ problem: slim(p), tests }) });
    });
  }

  // ---- Python via Pyodide (kept alive between runs; recreated after a timeout) ----
  let pyWorker = null; let pyReady = null;
  function startPy() {
    pyWorker = new Worker('py-worker.js');
    pyReady = new Promise((resolve, reject) => {
      pyWorker.onmessage = (e) => { if (e.data.t === 'ready') resolve(); else if (e.data.t === 'initerror') reject(new Error(e.data.msg)); };
      pyWorker.postMessage({ t: 'init', version: PYODIDE_VERSION });
    });
    pyReady.catch(() => {});
  }
  async function runPy(code, p, tests, onStatus) {
    if (!pyWorker) startPy();
    try {
      if (onStatus) onStatus('Loading Python (first time only, a few seconds)...');
      await pyReady;
    } catch (e) {
      pyWorker = null;
      return { status: 'Unavailable', cases: [], stdout: '', message: 'Could not load the Python runtime (it is downloaded from a CDN). Check your internet connection and try again.\n' + e.message, passed: 0, total: tests.length, maxMs: 0 };
    }
    const w = pyWorker;
    return new Promise((resolve) => {
      const recs = {}; let fatal = null; let out = ''; let done = false; let timedOut = false;
      const end = () => { if (done) return; done = true; clearTimeout(timer); resolve(finish(p, tests, recs, fatal, out, timedOut, 'The Python program stopped before producing a result.')); };
      const timer = setTimeout(() => { timedOut = true; w.terminate(); pyWorker = null; end(); }, RUN_TIMEOUT_MS);
      w.onmessage = (e) => {
        const m = e.data;
        if (m.t === 'rec') { try { const r = JSON.parse(m.line); if (r.fatal) fatal = r; else recs[r.i] = r; } catch (_) {} }
        else if (m.t === 'out') out += m.s + '\n';
        else if (m.t === 'done') end();
      };
      w.postMessage({ t: 'run', code, input: JSON.stringify({ problem: slim(p), tests }) });
    });
  }

  window.api = {
    web: true,
    runCode: async (payload) => {
      const { lang, code, problem, tests } = payload;
      if (lang === 'javascript') return runJs(code, problem, tests);
      if (lang === 'python') return runPy(code, problem, tests, payload.onStatus);
      return { status: 'Unavailable', cases: [], stdout: '', message: 'Java and C++ run only in the desktop app.', passed: 0, total: tests.length, maxMs: 0 };
    },
    detectToolchains: async () => ({ python: true, javascript: true, java: null, cpp: null }),
    monacoPath: async () => MONACO_BASE,
    openExternal: async (u) => { window.open(u, '_blank', 'noopener'); },
  };
})();
