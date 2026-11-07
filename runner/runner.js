'use strict';
const { spawn, spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { compare } = require('./compare');
const gen = require('./gen');

const IS_WIN = process.platform === 'win32';
const RUN_TIMEOUT_MS = 10000;
const COMPILE_TIMEOUT_MS = 60000;

function env() {
  const e = Object.assign({}, process.env);
  if (!IS_WIN) {
    // GUI apps on macOS start with a minimal PATH; add the usual places toolchains live.
    const extra = ['/opt/homebrew/bin', '/usr/local/bin', '/usr/bin', '/bin', '/usr/local/opt/openjdk/bin', '/opt/homebrew/opt/openjdk/bin'];
    e.PATH = (e.PATH ? e.PATH + ':' : '') + extra.join(':');
  }
  return e;
}

function killTree(child) {
  try {
    if (IS_WIN) spawnSync('taskkill', ['/pid', String(child.pid), '/T', '/F'], { windowsHide: true });
    else process.kill(-child.pid, 'SIGKILL');
  } catch (_) {
    try { child.kill('SIGKILL'); } catch (_) {}
  }
}

function exec(cmd, args, opts = {}) {
  return new Promise((resolve) => {
    let stdout = '';
    let stderr = '';
    let timedOut = false;
    let child;
    try {
      child = spawn(cmd, args, {
        cwd: opts.cwd,
        env: Object.assign(env(), opts.env || {}),
        windowsHide: true,
        detached: !IS_WIN,
        stdio: ['ignore', 'pipe', 'pipe'],
      });
    } catch (e) {
      resolve({ code: -1, signal: null, stdout, stderr: String(e), timedOut: false, spawnError: true });
      return;
    }
    const cap = 300000;
    child.stdout.on('data', (d) => { if (stdout.length < cap) stdout += d.toString(); });
    child.stderr.on('data', (d) => { if (stderr.length < cap) stderr += d.toString(); });
    const timer = setTimeout(() => { timedOut = true; killTree(child); }, opts.timeout || RUN_TIMEOUT_MS);
    child.on('error', (e) => { clearTimeout(timer); resolve({ code: -1, signal: null, stdout, stderr: stderr + String(e), timedOut, spawnError: true }); });
    child.on('close', (code, signal) => { clearTimeout(timer); resolve({ code, signal, stdout, stderr, timedOut }); });
  });
}

// ---------- toolchain detection ----------
let toolchains = null;

async function detectToolchains(force) {
  if (toolchains && !force) return toolchains;
  const t = { python: null, javascript: { cmd: process.execPath, args: [], env: { ELECTRON_RUN_AS_NODE: '1' } }, java: null, cpp: null };

  const pyCandidates = IS_WIN ? [['py', '-3'], ['python'], ['python3']] : [['python3'], ['python']];
  for (const c of pyCandidates) {
    const r = await exec(c[0], [...c.slice(1), '--version'], { timeout: 8000 });
    if (r.code === 0 && /Python 3/.test(r.stdout + r.stderr)) { t.python = { cmd: c[0], args: c.slice(1) }; break; }
  }

  const javac = await exec('javac', ['-version'], { timeout: 8000 });
  const java = await exec('java', ['-version'], { timeout: 8000 });
  if (javac.code === 0 && java.code === 0) t.java = { javac: 'javac', java: 'java' };

  for (const c of ['g++', 'clang++']) {
    const r = await exec(c, ['--version'], { timeout: 8000 });
    if (r.code === 0) { t.cpp = { cmd: c }; break; }
  }
  toolchains = t;
  return t;
}

const INSTALL_HINT = {
  python: IS_WIN ? 'Install Python 3 from python.org (tick "Add python.exe to PATH"), then restart the app.' : 'Install Python 3 (for example "brew install python" or from python.org), then restart the app.',
  java: IS_WIN ? 'Install a JDK (for example Temurin 21 from adoptium.net) and make sure javac is on PATH, then restart the app.' : 'Install a JDK (for example "brew install openjdk"), make sure javac is on PATH, then restart the app.',
  cpp: IS_WIN ? 'Install MinGW-w64 / MSYS2 so that g++ is on PATH, then restart the app.' : 'Install the Xcode command line tools ("xcode-select --install") so that clang++ is available, then restart the app.',
};

// ---------- helpers ----------
function cleanPaths(text, dir) {
  return String(text || '')
    .split('\n').filter((l) => !/^Picked up (JAVA_TOOL_OPTIONS|_JAVA_OPTIONS|JDK_JAVA_OPTIONS)/.test(l)).join('\n').split(dir + path.sep).join('').split(dir).join('').replace(/\r/g, '').trim();
}

function trunc(s, n) {
  s = String(s == null ? '' : s);
  return s.length > n ? s.slice(0, n) + '\n... (output truncated)' : s;
}

function rmrf(dir) {
  try { fs.rmSync(dir, { recursive: true, force: true }); } catch (_) {}
}

function parseJsonl(text) {
  const recs = {};
  let fatal = null;
  for (const line of text.split('\n')) {
    if (!line.trim()) continue;
    try {
      const r = JSON.parse(line);
      if (r.fatal) fatal = r;
      else recs[r.i] = r;
    } catch (_) { /* partial line from a killed process */ }
  }
  return { recs, fatal };
}

// ---------- main entry ----------
// payload: { lang, code, problem:{kind,fn,params,ret,inplace,cmp,design,rt}, tests:[{in, expected}] }
async function runCode(payload) {
  const { lang, code, problem: p, tests } = payload;
  const tc = await detectToolchains();
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lc150-'));
  const result = { status: 'Accepted', cases: [], stdout: '', message: '', passed: 0, total: tests.length, maxMs: 0 };
  try {
    let run; // { cmd, args, env }
    let resultsFile;
    if (lang === 'python') {
      if (!tc.python) return unavailable(result, 'Python 3 was not found on this computer. ' + INSTALL_HINT.python);
      fs.writeFileSync(path.join(dir, 'solution.py'), code);
      fs.copyFileSync(path.join(__dirname, 'harness.py'), path.join(dir, 'harness.py'));
      fs.writeFileSync(path.join(dir, 'input.json'), JSON.stringify({ problem: slim(p), tests }));
      run = { cmd: tc.python.cmd, args: [...tc.python.args, 'harness.py'] };
      resultsFile = 'results.jsonl';
    } else if (lang === 'javascript') {
      fs.writeFileSync(path.join(dir, 'solution.js'), code);
      fs.copyFileSync(path.join(__dirname, 'harness.js'), path.join(dir, 'harness.js'));
      fs.writeFileSync(path.join(dir, 'input.json'), JSON.stringify({ problem: slim(p), tests }));
      run = { cmd: tc.javascript.cmd, args: ['harness.js'], env: tc.javascript.env };
      resultsFile = 'results.jsonl';
    } else if (lang === 'java') {
      if (!tc.java) return unavailable(result, 'A JDK (javac + java) was not found on this computer. ' + INSTALL_HINT.java);
      fs.writeFileSync(path.join(dir, 'Main.java'), gen.genJava(p, code));
      fs.writeFileSync(path.join(dir, 'input.txt'), gen.encodeInput(p, tests));
      const c = await exec(tc.java.javac, ['-encoding', 'UTF-8', '-nowarn', '-d', 'out', 'Main.java'], { cwd: dir, timeout: COMPILE_TIMEOUT_MS });
      if (c.code !== 0) return compileError(result, cleanPaths(c.stderr || c.stdout, dir));
      run = { cmd: tc.java.java, args: ['-Xmx1g', '-cp', 'out', 'Main'] };
      resultsFile = 'results.txt';
    } else if (lang === 'cpp') {
      if (!tc.cpp) return unavailable(result, 'A C++ compiler (g++ or clang++) was not found on this computer. ' + INSTALL_HINT.cpp);
      fs.writeFileSync(path.join(dir, 'main.cpp'), gen.genCpp(p, code));
      fs.writeFileSync(path.join(dir, 'input.txt'), gen.encodeInput(p, tests));
      const exe = IS_WIN ? 'prog.exe' : 'prog';
      const flags = ['-std=c++17', '-O2', '-o', exe, 'main.cpp'];
      if (IS_WIN) flags.push('-Wl,--stack,268435456');
      else if (process.platform === 'darwin') flags.push('-Wl,-stack_size,0x10000000');
      const c = await exec(tc.cpp.cmd, flags, { cwd: dir, timeout: COMPILE_TIMEOUT_MS });
      if (c.code !== 0) return compileError(result, cleanPaths(c.stderr || c.stdout, dir));
      run = { cmd: path.join(dir, exe), args: [] };
      resultsFile = 'results.txt';
    } else {
      return unavailable(result, 'Unknown language: ' + lang);
    }

    const r = await exec(run.cmd, run.args, { cwd: dir, timeout: RUN_TIMEOUT_MS, env: run.env });
    result.stdout = trunc(cleanPaths(r.stdout, dir), 6000);
    let text = '';
    try { text = fs.readFileSync(path.join(dir, resultsFile), 'utf8'); } catch (_) {}

    let recs = {};
    let fatal = null;
    if (resultsFile === 'results.jsonl') ({ recs, fatal } = parseJsonl(text));
    else recs = gen.parseResults(p, text);

    if (fatal) {
      result.status = fatal.syntax ? 'Compile Error' : 'Runtime Error';
      result.message = cleanPaths(fatal.fatal, dir);
      result.cases = tests.map((t, i) => ({ index: i, status: 'skipped' }));
      return result;
    }
    if (r.spawnError) {
      return unavailable(result, 'Could not start the program: ' + cleanPaths(r.stderr, dir));
    }

    let firstMissing = true;
    for (let i = 0; i < tests.length; i++) {
      const t = tests[i];
      const rec = recs[i];
      let c;
      if (!rec) {
        if (r.timedOut) c = { index: i, status: firstMissing ? 'tle' : 'skipped' };
        else if (firstMissing) c = { index: i, status: 'error', message: crashMessage(r, dir) };
        else c = { index: i, status: 'skipped' };
        firstMissing = false;
      } else if (!rec.ok) {
        c = { index: i, status: 'error', message: cleanPaths(rec.err, dir) };
      } else {
        const ok = compare(p.cmp || 'exact', rec.out, t.expected, p.kind === 'func' ? t.in : null);
        c = { index: i, status: ok ? 'pass' : 'fail', actual: rec.out, ms: rec.ms };
        if (ok) result.passed++;
        if (typeof rec.ms === 'number') result.maxMs = Math.max(result.maxMs, rec.ms);
      }
      result.cases.push(c);
    }
    const has = (s) => result.cases.some((c) => c.status === s);
    if (has('error')) {
      result.status = 'Runtime Error';
      result.message = result.cases.find((c) => c.status === 'error').message;
    } else if (has('tle')) result.status = 'Time Limit Exceeded';
    else if (has('fail')) result.status = 'Wrong Answer';
    else result.status = 'Accepted';
    return result;
  } finally {
    rmrf(dir);
  }
}

function crashMessage(r, dir) {
  const err = cleanPaths(r.stderr, dir);
  if (r.signal) return 'The program crashed (' + r.signal + ').' + (err ? '\n' + trunc(err, 1500) : '');
  if (r.code) return 'The program exited with code ' + r.code + '.' + (err ? '\n' + trunc(err, 1500) : '');
  return err ? trunc(err, 1500) : 'The program stopped before producing a result.';
}

function slim(p) {
  return { kind: p.kind, fn: p.fn, params: p.params, ret: p.ret, inplace: p.inplace, design: p.design, rt: p.rt, post: p.post };
}

function unavailable(result, message) {
  result.status = 'Unavailable';
  result.message = message;
  return result;
}

function compileError(result, message) {
  result.status = 'Compile Error';
  result.message = trunc(message, 4000);
  return result;
}

module.exports = { runCode, detectToolchains };
