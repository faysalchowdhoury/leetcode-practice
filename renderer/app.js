'use strict';
(function () {
  const $ = (s) => document.querySelector(s);
  const GROUPS = window.GROUPS;
  const PROBS = window.PROBLEMS;
  const BY_ID = {};
  PROBS.forEach((p) => { BY_ID[p.id] = p; });
  const LANGS = Lang.LANGS;
  const TAG_LABEL = { B: 'Both', N: 'NeetCode only', L: 'LeetCode only' };
  const TAG_SHORT = { B: 'Both', N: 'N', L: 'L' };

  // ---------- persistence (all guarded) ----------
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (_) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (_) {} },
  };
  let solved = store.get('lc.solved', {});
  let state = store.get('lc.state', { id: PROBS[0].id, lang: 'python', open: [0] });
  if (!BY_ID[state.id]) state.id = PROBS[0].id;
  let listFilter = 'all';
  let query = '';
  let onlyUnsolved = false;
  let toolchains = null;
  const hasApi = !!window.api;

  const saveState = () => store.set('lc.state', state);
  const codeKey = (id, lang) => 'lc.code.' + id + '.' + lang;
  const curP = () => BY_ID[state.id];

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function inl(s) { return esc(s).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>'); }
  function J(v) { return JSON.stringify(v); }

  // ---------- filters ----------
  function visible(p) {
    if (listFilter === 'neet' && p.tag === 'L') return false;
    if (listFilter === 'leet' && p.tag === 'N') return false;
    if (listFilter === 'B' && p.tag !== 'B') return false;
    if (listFilter === 'N' && p.tag !== 'N') return false;
    if (listFilter === 'L' && p.tag !== 'L') return false;
    if (onlyUnsolved && solved[p.id]) return false;
    if (query) {
      const q = query.toLowerCase();
      if (!(p.title.toLowerCase().includes(q) || String(p.lc || '') === q || String(p.lc || '').startsWith(q))) return false;
    }
    return true;
  }

  function inList(p) { // for progress/counts: list filter only
    if (listFilter === 'neet') return p.tag !== 'L';
    if (listFilter === 'leet') return p.tag !== 'N';
    if (listFilter === 'B' || listFilter === 'N' || listFilter === 'L') return p.tag === listFilter;
    return true;
  }

  // ---------- sidebar ----------
  function renderSidebar() {
    const box = $('#group-list');
    const searching = !!query;
    let html = '';
    let shown = 0;
    GROUPS.forEach((g) => {
      const all = g.ids.map((i) => BY_ID[i]).filter(inList);
      const vis = all.filter(visible);
      if (!all.length) return;
      if ((searching || onlyUnsolved) && !vis.length) return;
      shown++;
      const done = all.filter((p) => solved[p.id]).length;
      const open = searching || state.open.includes(g.index);
      html += '<div class="group' + (open ? ' open' : '') + '" data-g="' + g.index + '">' +
        '<div class="group-head"><span class="caret">&#9654;</span><span class="gnum">' + (g.index + 1) + '</span>' +
        '<span class="gname">' + esc(g.name) + '</span><span class="gcount' + (done === all.length ? ' done' : '') + '">' + done + '/' + all.length + '</span></div>' +
        '<div class="group-items">' +
        vis.map((p) => '<div class="item' + (p.id === state.id ? ' active' : '') + '" data-id="' + p.id + '">' +
          '<span class="tick">' + (solved[p.id] ? '&#10003;' : '') + '</span>' +
          '<span class="ititle">' + esc(p.title) + '</span>' +
          '<span class="tag tag-' + p.tag + '" title="' + TAG_LABEL[p.tag] + '">' + TAG_SHORT[p.tag] + '</span>' +
          '<span class="idiff diff-' + p.diff + '">' + p.diff[0] + '</span></div>').join('') +
        '</div></div>';
    });
    box.innerHTML = shown ? html : '<div class="empty">No problems match.</div>';
    updateProgress();
  }

  function updateProgress() {
    const list = PROBS.filter(inList);
    const done = list.filter((p) => solved[p.id]).length;
    $('#progress-text').textContent = done + ' / ' + list.length + ' solved';
    $('#progress-fill').style.width = (list.length ? (100 * done / list.length) : 0) + '%';
  }

  $('#group-list').addEventListener('click', (e) => {
    const item = e.target.closest('.item');
    if (item) { selectProblem(+item.dataset.id); return; }
    const head = e.target.closest('.group-head');
    if (head) {
      const gi = +head.parentElement.dataset.g;
      const k = state.open.indexOf(gi);
      if (k >= 0) state.open.splice(k, 1); else state.open.push(gi);
      saveState();
      head.parentElement.classList.toggle('open');
    }
  });

  // filter dropdown
  (function () {
    const sel = $('#filter-list');
    const c = (f) => PROBS.filter(f).length;
    const opts = [
      ['all', 'All problems (' + PROBS.length + ')'],
      ['neet', 'NeetCode list (Both + NeetCode only: ' + c((p) => p.tag !== 'L') + ')'],
      ['leet', 'LeetCode list (Both + LeetCode only: ' + c((p) => p.tag !== 'N') + ')'],
      ['B', 'Both only (' + c((p) => p.tag === 'B') + ')'],
      ['N', 'NeetCode only (' + c((p) => p.tag === 'N') + ')'],
      ['L', 'LeetCode only (' + c((p) => p.tag === 'L') + ')'],
    ];
    sel.innerHTML = opts.map((o) => '<option value="' + o[0] + '">' + o[1] + '</option>').join('');
    sel.addEventListener('change', () => { listFilter = sel.value; renderSidebar(); });
  })();
  $('#search').addEventListener('input', (e) => { query = e.target.value.trim(); renderSidebar(); });
  $('#only-unsolved').addEventListener('change', (e) => { onlyUnsolved = e.target.checked; renderSidebar(); });

  // ---------- problem pane ----------
  function exampleText(p, t) {
    if (p.kind === 'design') {
      return ['<b>Operations:</b> ' + esc(J(t.in.ops)), '<b>Arguments:</b> ' + esc(J(t.in.args)), '<b>Output:</b> ' + esc(J(t.expected))].join('\n');
    }
    if (p.kind === 'roundtrip') {
      return '<b>Input:</b> ' + esc(J(t.in)) + '\n<b>Output:</b> same as input after ' + esc((p.rt && (p.rt.enc || p.rt.encode)) || 'encode') + ' then decode';
    }
    const args = (p.params || []).map((pr, i) => esc(pr[0]) + ' = ' + esc(J(t.in[i]))).join(', ');
    const out = p.inplace != null && p.inplace !== false && p.ret === 'void'
      ? esc(J(t.expected)) + '  <i>(the modified argument)</i>' : esc(J(t.expected));
    return '<b>Input:</b> ' + args + '\n<b>Output:</b> ' + out;
  }

  function renderDesc(text) {
    const lines = text.split('\n');
    let out = '', inList_ = false;
    const closeList = () => { if (inList_) { out += '</ul>'; inList_ = false; } };
    lines.forEach((ln) => {
      if (/^\s*[-*] /.test(ln)) { if (!inList_) { out += '<ul>'; inList_ = true; } out += '<li>' + inl(ln.replace(/^\s*[-*] /, '')) + '</li>'; return; }
      closeList();
      if (!ln.trim()) return;
      if (/^constraints:?$/i.test(ln.trim())) out += '<p class="cons-head">Constraints</p>';
      else out += '<p>' + inl(ln) + '</p>';
    });
    closeList();
    return out;
  }

  const LINKS = window.LINKS || {};
  function lcUrl(p) { const l = LINKS[p.id]; return l && l.lc ? 'https://leetcode.com/problems/' + l.lc + '/' : null; }
  function ncUrl(p) { const l = LINKS[p.id]; return l && l.nc ? 'https://neetcode.io/problems/' + l.nc + '/' : 'https://neetcode.io/practice'; }
  $('#problem').addEventListener('click', (e) => {
    const a = e.target.closest('a[data-ext]');
    if (!a) return;
    e.preventDefault();
    if (hasApi) window.api.openExternal(a.href); else window.open(a.href);
  });

  function renderProblem() {
    const p = curP();
    const g = GROUPS[p.group];
    let h = '<h1 class="p-title"><span>' + esc(p.title) + '</span>' + (solved[p.id] ? '<span class="solved">&#10003; Solved</span>' : '') + '</h1>';
    h += '<div class="chips"><span class="chip diff diff-' + p.diff + '">' + p.diff + '</span>' +
      '<span class="chip tagchip-' + p.tag + '">' + TAG_LABEL[p.tag] + '</span>' +
      (p.lc ? '<span class="chip">LeetCode #' + p.lc + '</span>' : '') +
      '<span class="chip">' + esc(g.name) + '</span></div>';
    h += '<div class="links">' +
      '<a href="' + lcUrl(p) + '" data-ext="1">LeetCode &#8599;</a>' +
      '<a href="' + ncUrl(p) + '" data-ext="1">NeetCode' + (LINKS[p.id] && LINKS[p.id].nc ? '' : ' (list)') + ' &#8599;</a>' + '</div>';
    h += '<div class="desc">' + renderDesc(p.desc) + '</div>';
    const n = Math.min(p.ex || 0, p.tests.length);
    for (let i = 0; i < n; i++) h += '<div class="ex"><h4>Example ' + (i + 1) + '</h4><pre>' + exampleText(p, p.tests[i]) + '</pre></div>';
    if (g.tip) h += '<div class="tip"><b>' + esc(g.name) + ':</b> ' + esc(g.tip) + '</div>';
    if (p.inplace != null && p.inplace !== false) h += '<p style="color:var(--muted);font-size:12.5px">Modify the argument in place; it is checked after your function returns.</p>';
    if (p.hint) h += '<details class="hint"><summary>Hint</summary><p>' + inl(p.hint) + '</p></details>';
    const el = $('#problem');
    el.innerHTML = h;
    el.scrollTop = 0;
  }

  // ---------- editor ----------
  let editor = null, monacoRef = null, textarea = null;
  let suppress = false;

  function getCode() { return editor ? editor.getValue() : (textarea ? textarea.value : ''); }
  function setCode(v) {
    suppress = true;
    if (editor) editor.setValue(v); else if (textarea) textarea.value = v;
    suppress = false;
  }
  function onCodeChange() {
    if (suppress) return;
    store.set(codeKey(state.id, state.lang), getCode());
  }

  function setupLangSelect() {
    const p = curP();
    const sel = $('#lang');
    sel.innerHTML = LANGS.map((l) => {
      const webOnly = hasApi && window.api.web && (l.id === 'java' || l.id === 'cpp');
      const ok = Lang.supports(p, l.id) && !webOnly;
      return '<option value="' + l.id + '"' + (ok ? '' : ' disabled') + '>' + l.label + (ok ? '' : (hasApi && window.api.web && (l.id === 'java' || l.id === 'cpp') ? ' (desktop app only)' : ' (not available)')) + '</option>';
    }).join('');
    if (!Lang.supports(p, state.lang)) state.lang = 'python';
    sel.value = state.lang;
    const w = $('#lang-warning');
    const unsup = LANGS.filter((l) => !Lang.supports(p, l.id));
    if (hasApi && window.api.web) {
      w.textContent = 'Java and C++: desktop app only';
      w.classList.remove('hidden');
    } else if (unsup.length) {
      w.textContent = 'Java and C++ are not offered for this problem (uses linked structures, design classes or special output).';
      w.classList.remove('hidden');
    } else w.classList.add('hidden');
  }

  function loadCode() {
    const p = curP();
    const saved = store.get(codeKey(p.id, state.lang), null);
    const code = typeof saved === 'string' ? saved : Lang.starter(p, state.lang);
    const l = LANGS.find((x) => x.id === state.lang);
    if (editor && monacoRef) monacoRef.editor.setModelLanguage(editor.getModel(), l.monaco);
    setCode(code);
  }

  function selectProblem(id) {
    state.id = id;
    const g = curP().group;
    if (!state.open.includes(g)) state.open.push(g);
    saveState();
    setupLangSelect();
    renderProblem();
    loadCode();
    renderSidebar();
    showCases();
    const act = document.querySelector('.item.active');
    if (act) act.scrollIntoView({ block: 'nearest' });
  }

  $('#lang').addEventListener('change', (e) => {
    state.lang = e.target.value;
    saveState();
    loadCode();
  });
  $('#btn-reset').addEventListener('click', () => {
    if (!confirm('Reset your code for this problem and language to the starter code?')) return;
    try { localStorage.removeItem(codeKey(state.id, state.lang)); } catch (_) {}
    loadCode();
  });

  function initFallbackEditor(msg) {
    const host = $('#editor');
    host.innerHTML = '';
    textarea = document.createElement('textarea');
    textarea.spellcheck = false;
    textarea.addEventListener('input', onCodeChange);
    textarea.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        const s = textarea.selectionStart;
        textarea.setRangeText('    ', s, textarea.selectionEnd, 'end');
        onCodeChange();
      }
    });
    host.appendChild(textarea);
    if (msg) console.warn(msg);
  }

  async function initEditor() {
    let base = null;
    try { if (hasApi) base = await window.api.monacoPath(); } catch (_) {}
    if (!base) { initFallbackEditor('Monaco path not available'); return; }
    base = base.replace(/\\/g, '/');
    const url = /^https?:/.test(base) ? base : 'file://' + (base.startsWith('/') ? '' : '/') + base.split('/').map(encodeURIComponent).join('/').replace(/%3A/g, ':');
    await new Promise((resolve) => {
      const s = document.createElement('script');
      s.src = url + '/loader.js';
      s.onload = () => {
        try {
          window.MonacoEnvironment = {
            getWorkerUrl() {
              const code = "self.MonacoEnvironment={baseUrl:'" + url + "/../'};importScripts('" + url + "/base/worker/workerMain.js');";
              return 'data:text/javascript;charset=utf-8,' + encodeURIComponent(code);
            },
          };
          window.require.config({ paths: { vs: url } });
          window.require(['vs/editor/editor.main'], () => {
            monacoRef = window.monaco;
            editor = monacoRef.editor.create($('#editor'), {
              value: '', language: 'python', theme: 'vs-dark', automaticLayout: true,
              minimap: { enabled: false }, fontSize: 14, scrollBeyondLastLine: false,
              tabSize: 4, insertSpaces: true, fontLigatures: false, padding: { top: 8 },
            });
            editor.onDidChangeModelContent(onCodeChange);
            editor.addCommand(monacoRef.KeyMod.CtrlCmd | monacoRef.KeyCode.Enter, () => run(true));
            editor.addCommand(monacoRef.KeyMod.CtrlCmd | monacoRef.KeyCode.Quote, () => run(false));
            resolve();
          }, () => { initFallbackEditor('Monaco failed to load'); resolve(); });
        } catch (e) { initFallbackEditor(String(e)); resolve(); }
      };
      s.onerror = () => { initFallbackEditor('loader.js failed'); resolve(); };
      document.head.appendChild(s);
    });
  }

  // ---------- results ----------
  let lastRun = null; // { mode, res, tests, sel }
  let activeTab = 'cases';

  function setTab(t) {
    activeTab = t;
    document.querySelectorAll('#result-tabs .tab').forEach((b) => b.classList.toggle('active', b.dataset.tab === t));
    if (t === 'cases') showCases(); else showResult();
  }
  document.querySelectorAll('#result-tabs .tab').forEach((b) => b.addEventListener('click', () => setTab(b.dataset.tab)));

  function inputText(p, t) {
    if (p.kind === 'design') return 'ops: ' + J(t.in.ops) + '\nargs: ' + J(t.in.args);
    if (p.kind === 'roundtrip') return J(t.in);
    return (p.params || []).map((pr, i) => pr[0] + ' = ' + J(t.in[i])).join('\n');
  }

  let casesSel = 0;
  function showCases() {
    activeTab = 'cases';
    document.querySelectorAll('#result-tabs .tab').forEach((b) => b.classList.toggle('active', b.dataset.tab === 'cases'));
    const p = curP();
    const n = Math.min(3, p.tests.length);
    if (casesSel >= n) casesSel = 0;
    let h = '<div class="pills">';
    for (let i = 0; i < n; i++) h += '<button class="pill' + (i === casesSel ? ' sel' : '') + '" data-c="' + i + '">Case ' + (i + 1) + '</button>';
    h += '</div>';
    const t = p.tests[casesSel];
    h += '<div class="field"><label>Input</label><div class="box">' + esc(inputText(p, t)) + '</div></div>';
    h += '<div class="field"><label>Expected output</label><div class="box">' + esc(J(t.expected)) + '</div></div>';
    h += '<div class="substat">Run checks Cases 1-3. Submit checks all ' + p.tests.length + ' tests.</div>';
    const body = $('#result-body');
    body.innerHTML = h;
    body.querySelectorAll('.pill').forEach((b) => b.addEventListener('click', () => { casesSel = +b.dataset.c; showCases(); }));
  }

  function showResult() {
    const body = $('#result-body');
    if (!lastRun) { body.innerHTML = '<div class="empty">Run or submit your code to see results here.</div>'; return; }
    const { mode, res, tests, sel } = lastRun;
    const p = curP();
    const cls = res.status === 'Accepted' ? 'ok' : (res.status === 'Unavailable' ? 'warnc' : 'bad');
    let h = '<div class="status ' + cls + '">' + esc(res.status) + '</div>';
    if (res.status === 'Compile Error' || res.status === 'Unavailable' || (res.status === 'Runtime Error' && !res.cases.some((c) => c.status === 'error' || c.status === 'pass' || c.status === 'fail'))) {
      h += '<div class="msg-pre">' + esc(res.message || '') + '</div>';
      if (res.stdout) h += '<div class="field" style="margin-top:10px"><label>Stdout</label><div class="box">' + esc(res.stdout) + '</div></div>';
      body.innerHTML = h;
      return;
    }
    h += '<div class="substat">' + res.passed + ' / ' + res.total + ' test cases passed' + (res.maxMs ? ' &middot; slowest case ' + Math.round(res.maxMs) + ' ms' : '') +
      (mode === 'run' ? ' &middot; Run (examples only)' : ' &middot; Submit') + '</div>';
    h += '<div class="pills">' + res.cases.map((c, i) => '<button class="pill' + (i === sel ? ' sel' : '') + '" data-c="' + i + '"><span class="dot ' + c.status + '"></span>Case ' + (i + 1) + '</button>').join('') + '</div>';
    const c = res.cases[sel];
    if (c) {
      const t = tests[sel];
      if (c.status === 'skipped') h += '<div class="substat">Not run (an earlier case stopped the program).</div>';
      h += '<div class="field"><label>Input</label><div class="box">' + esc(inputText(p, t)) + '</div></div>';
      if (c.status === 'error') h += '<div class="field"><label>Error</label><div class="box err">' + esc(c.message || '') + '</div></div>';
      else if (c.status === 'tle') h += '<div class="field"><label>Error</label><div class="box err">Time limit exceeded (10 seconds for the whole run).</div></div>';
      else if (c.status === 'pass' || c.status === 'fail') {
        h += '<div class="field"><label>Your output</label><div class="box ' + (c.status === 'pass' ? 'good' : 'err') + '">' + esc(J(c.actual)) + '</div></div>';
        h += '<div class="field"><label>Expected output</label><div class="box">' + esc(J(t.expected)) + '</div></div>';
      }
    }
    if (res.stdout) h += '<div class="field"><label>Stdout</label><div class="box">' + esc(res.stdout) + '</div></div>';
    body.innerHTML = h;
    body.querySelectorAll('.pill').forEach((b) => b.addEventListener('click', () => { lastRun.sel = +b.dataset.c; showResult(); }));
  }

  function showBusy(label) {
    activeTab = 'result';
    document.querySelectorAll('#result-tabs .tab').forEach((b) => b.classList.toggle('active', b.dataset.tab === 'result'));
    $('#result-body').innerHTML = '<div class="status"><span class="spinner"></span>' + label + '</div>';
  }

  let running = false;
  async function run(submit) {
    if (running) return;
    if (!hasApi) { alert('Running code only works inside the desktop app.'); return; }
    const p = curP();
    const tests = submit ? p.tests : p.tests.slice(0, Math.min(3, p.tests.length));
    running = true;
    $('#btn-run').disabled = true; $('#btn-submit').disabled = true;
    showBusy(submit ? 'Running all ' + tests.length + ' tests...' : 'Running...');
    const onStatus = (m) => showBusy(m);
    let res;
    try {
      res = await window.api.runCode({ lang: state.lang, code: getCode(), problem: p, tests, ...(window.api.web ? { onStatus } : {}) });
    } catch (e) {
      res = { status: 'Runtime Error', cases: [], stdout: '', message: String(e && e.message || e), passed: 0, total: tests.length, maxMs: 0 };
    }
    running = false;
    $('#btn-run').disabled = false; $('#btn-submit').disabled = false;
    let sel = res.cases.findIndex((c) => c.status !== 'pass');
    if (sel < 0) sel = 0;
    lastRun = { mode: submit ? 'submit' : 'run', res, tests, sel };
    if (submit && res.status === 'Accepted') {
      solved[p.id] = true;
      store.set('lc.solved', solved);
      renderSidebar();
      renderProblem();
    }
    setTab('result');
  }
  $('#btn-run').addEventListener('click', () => run(false));
  $('#btn-submit').addEventListener('click', () => run(true));

  // ---------- navigation ----------
  function orderedIds() { return GROUPS.flatMap((g) => g.ids).filter((i) => visible(BY_ID[i]) || i === state.id); }
  function step(d) {
    const ids = orderedIds();
    const k = ids.indexOf(state.id);
    const n = ids[(k + d + ids.length) % ids.length];
    selectProblem(n);
  }
  $('#btn-prev').addEventListener('click', () => step(-1));
  $('#btn-next').addEventListener('click', () => step(1));
  $('#btn-random').addEventListener('click', () => {
    const pool = PROBS.filter((p) => inList(p) && !solved[p.id] && p.id !== state.id);
    if (!pool.length) return;
    selectProblem(pool[Math.floor(Math.random() * pool.length)].id);
  });

  // ---------- resizers ----------
  function drag(el, onMove) {
    el.addEventListener('mousedown', (e) => {
      e.preventDefault();
      const mv = (ev) => onMove(ev);
      const up = () => { document.removeEventListener('mousemove', mv); document.removeEventListener('mouseup', up); document.body.style.userSelect = ''; };
      document.body.style.userSelect = 'none';
      document.addEventListener('mousemove', mv);
      document.addEventListener('mouseup', up);
    });
  }
  drag($('#rz-v'), (e) => {
    const r = $('#main').getBoundingClientRect();
    const w = Math.max(280, Math.min(r.width - 340, e.clientX - r.left - 8));
    $('#left').style.width = w + 'px';
  });
  drag($('#rz-h'), (e) => {
    const r = $('#right').getBoundingClientRect();
    const h = Math.max(90, Math.min(r.height - 200, r.bottom - e.clientY));
    $('#results').style.height = h + 'px';
  });

  // ---------- boot ----------
  async function boot() {
    renderSidebar();
    setupLangSelect();
    renderProblem();
    showCases();
    await initEditor();
    loadCode();
    const act = document.querySelector('.item.active');
    if (act) act.scrollIntoView({ block: 'center' });
    if (hasApi) {
      try { toolchains = await window.api.detectToolchains(); } catch (_) {}
    }
  }
  boot();
})();
