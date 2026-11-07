// Test harness for JavaScript submissions. Runs the user's code inside a Worker with a large stack.
// Reads input.json + solution.js from the working directory and appends one JSON line per test to results.jsonl.
'use strict';
const { Worker, isMainThread, workerData } = require('worker_threads');
const fs = require('fs');
const vm = require('vm');
const path = require('path');

if (isMainThread) {
  const w = new Worker(__filename, {
    workerData: { dir: process.cwd() },
    resourceLimits: { stackSizeMb: 200, maxOldGenerationSizeMb: 2048 },
  });
  w.on('error', (e) => {
    try {
      fs.appendFileSync(path.join(process.cwd(), 'results.jsonl'), JSON.stringify({ fatal: String(e && e.stack ? e.stack : e).split('\n').slice(0, 4).join('\n') }) + '\n');
    } catch (_) {}
  });
  w.on('exit', () => process.exit(0));
} else {
  runAll(workerData.dir);
}

function runAll(dir) {
  const cfg = JSON.parse(fs.readFileSync(path.join(dir, 'input.json'), 'utf8'));
  const P = cfg.problem;
  const tests = cfg.tests;
  const fd = fs.openSync(path.join(dir, 'results.jsonl'), 'w');
  const emit = (rec) => fs.writeSync(fd, JSON.stringify(rec) + '\n');
  const code = fs.readFileSync(path.join(dir, 'solution.js'), 'utf8');
  const ptypes = (P.params || []).map((x) => x[1]);
  const usesGraph = ptypes.includes('Node');
  const usesNext = ptypes.includes('NextTree');
  const usesQuad = P.ret === 'QuadTree';

  // ---- data structures available to user code (same as the LeetCode editor) ----
  globalThis.ListNode = function ListNode(val, next) {
    this.val = val === undefined ? 0 : val;
    this.next = next === undefined ? null : next;
  };
  globalThis.TreeNode = function TreeNode(val, left, right) {
    this.val = val === undefined ? 0 : val;
    this.left = left === undefined ? null : left;
    this.right = right === undefined ? null : right;
  };
  globalThis._Node = function _Node(val, a, b) {
    this.val = val === undefined ? 0 : val;
    if (usesGraph) this.neighbors = a === undefined ? [] : a;
    else { this.next = a === undefined ? null : a; this.random = b === undefined ? null : b; }
  };
  globalThis.Node = function Node(a, b, c, d, e, f) {
    if (usesQuad) {
      this.val = a; this.isLeaf = b; this.topLeft = c === undefined ? null : c; this.topRight = d === undefined ? null : d;
      this.bottomLeft = e === undefined ? null : e; this.bottomRight = f === undefined ? null : f;
    } else {
      this.val = a === undefined ? 0 : a; this.left = b === undefined ? null : b; this.right = c === undefined ? null : c; this.next = d === undefined ? null : d;
    }
  };
  const ListNode = globalThis.ListNode, TreeNode = globalThis.TreeNode, _Node = globalThis._Node;
  const ctx = { orig: new Set() };

  // capture console output so the protocol file stays clean
  const logs = [];
  const fmt = (a) => (typeof a === 'string' ? a : (() => { try { return JSON.stringify(a); } catch (_) { return String(a); } })());
  console.log = (...args) => { logs.push(args.map(fmt).join(' ')); if (logs.length < 2000) process.stdout.write(args.map(fmt).join(' ') + '\n'); };
  console.info = console.log; console.warn = console.log; console.error = console.log;

  const mkList = (a) => { const d = new ListNode(0); let c = d; for (const v of a) { c.next = new ListNode(v); c = c.next; } return d.next; };
  const listOut = (h) => { const r = []; let n = 0; while (h != null) { r.push(h.val); h = h.next; if (++n > 2000000) throw new Error('The returned linked list seems to contain a cycle'); } return r; };
  const mkCycle = (a) => {
    const head = mkList(a[0]); const pos = a[1];
    if (pos >= 0 && head) { let t = head; for (let i = 0; i < pos; i++) t = t.next; let tail = head; while (tail.next) tail = tail.next; tail.next = t; }
    return head;
  };
  const mkTree = (a, Cls) => {
    Cls = Cls || TreeNode;
    if (!a || !a.length || a[0] === null) return null;
    const root = new Cls(a[0]); const q = [root]; let h = 0, i = 1;
    while (h < q.length && i < a.length) {
      const n = q[h++];
      if (i < a.length && a[i] !== null) { n.left = new Cls(a[i]); q.push(n.left); } i++;
      if (i < a.length && a[i] !== null) { n.right = new Cls(a[i]); q.push(n.right); } i++;
    }
    return root;
  };
  const nextOut = (root) => {
    const levels = [];
    if (root == null) return levels;
    let level = [root];
    while (level.length) {
      level.forEach((n, i) => {
        const want = i + 1 < level.length ? level[i + 1] : null;
        if ((n.next === undefined ? null : n.next) !== want) throw new Error('The next pointer of node ' + n.val + ' is wrong (it should point to ' + (want === null ? 'null' : want.val) + ')');
      });
      levels.push(level.map((n) => n.val));
      const nxt = [];
      for (const n of level) { if (n.left) nxt.push(n.left); if (n.right) nxt.push(n.right); }
      level = nxt;
    }
    return levels;
  };
  const quadOut = (root) => {
    const out = []; const q = [root]; let h = 0;
    while (h < q.length) {
      const n = q[h++];
      if (n == null) { out.push(null); continue; }
      out.push([n.isLeaf ? 1 : 0, n.isLeaf ? (n.val ? 1 : 0) : 1]);
      if (!n.isLeaf) q.push(n.topLeft, n.topRight, n.bottomLeft, n.bottomRight);
    }
    while (out.length && out[out.length - 1] === null) out.pop();
    return out;
  };
  const treeOut = (root) => {
    if (root == null) return [];
    const r = []; const q = [root]; let h = 0;
    while (h < q.length) {
      const n = q[h++];
      if (n == null) r.push(null); else { r.push(n.val); q.push(n.left); q.push(n.right); }
    }
    while (r.length && r[r.length - 1] === null) r.pop();
    return r;
  };
  const mkGraph = (adj) => {
    if (!adj.length) return null;
    const nodes = adj.map((_, i) => new _Node(i + 1, []));
    adj.forEach((nb, i) => { nodes[i].neighbors = nb.map((j) => nodes[j - 1]); });
    ctx.orig = new Set(nodes);
    return nodes[0];
  };
  const graphOut = (node) => {
    if (node == null) return [];
    const seen = new Set([node]); const q = [node]; let h = 0;
    while (h < q.length) { const n = q[h++]; for (const m of n.neighbors) if (!seen.has(m)) { seen.add(m); q.push(m); } }
    for (const n of seen) if (ctx.orig.has(n)) throw new Error('You returned the original nodes. Build a deep copy of the graph.');
    let size = 0; for (const n of seen) size = Math.max(size, n.val);
    const res = Array.from({ length: size }, () => []);
    for (const n of seen) res[n.val - 1] = n.neighbors.map((m) => m.val).sort((a, b) => a - b);
    return res;
  };
  const mkRand = (a) => {
    if (!a.length) return null;
    const nodes = a.map((x) => new _Node(x[0]));
    nodes.forEach((n, i) => { if (i + 1 < nodes.length) n.next = nodes[i + 1]; if (a[i][1] !== null) n.random = nodes[a[i][1]]; });
    ctx.orig = new Set(nodes);
    return nodes[0];
  };
  const randOut = (head) => {
    const nodes = []; const idx = new Map(); let n = head;
    while (n != null) {
      if (idx.has(n)) throw new Error('The returned list contains a cycle');
      if (ctx.orig.has(n)) throw new Error('You returned original nodes. Build a deep copy of the list.');
      idx.set(n, nodes.length); nodes.push(n); n = n.next;
    }
    return nodes.map((x) => {
      if (x.random == null) return [x.val, null];
      if (!idx.has(x.random)) throw new Error('A random pointer points outside the returned list');
      return [x.val, idx.get(x.random)];
    });
  };
  const clone = (v) => JSON.parse(JSON.stringify(v));
  const convIn = (t, v) => {
    switch (t) {
      case 'ListNode': return mkList(v);
      case 'ListNode[]': return v.map(mkList);
      case 'TreeNode': return mkTree(v);
      case 'Node': return mkGraph(v);
      case 'RandomList': return mkRand(v);
      case 'CycleList': return mkCycle(v);
      case 'NextTree': return mkTree(v, globalThis.Node);
      default: return clone(v);
    }
  };
  const convOut = (t, v) => {
    switch (t) {
      case 'ListNode': return listOut(v);
      case 'TreeNode': return treeOut(v);
      case 'Node': return graphOut(v);
      case 'RandomList': return randOut(v);
      case 'NextTree': return nextOut(v);
      case 'QuadTree': return quadOut(v);
      default: return v === undefined ? null : v;
    }
  };
  const fmtErr = (e) => {
    const name = e && e.name ? e.name : 'Error';
    const msg = e && e.message ? e.message : String(e);
    const lines = [name + ': ' + msg];
    const st = e && e.stack ? String(e.stack).split('\n') : [];
    for (const l of st) {
      const m = /solution\.js:(\d+):(\d+)/.exec(l);
      if (m) lines.push('  at line ' + m[1] + ', column ' + m[2]);
      if (lines.length > 5) break;
    }
    return lines.join('\n');
  };
  const now = () => Number(process.hrtime.bigint()) / 1e6;

  try {
    vm.runInThisContext(code, { filename: 'solution.js' });
  } catch (e) {
    emit({ fatal: fmtErr(e), syntax: e instanceof SyntaxError });
    fs.closeSync(fd);
    return;
  }
  const lookup = (name) => {
    try { return vm.runInThisContext('typeof ' + name + ' !== "undefined" ? ' + name + ' : undefined'); } catch (_) { return undefined; }
  };

  for (let idx = 0; idx < tests.length; idx++) {
    const t = tests[idx];
    try {
      let out, ms;
      if (P.kind === 'func') {
        const fn = lookup(P.fn);
        if (typeof fn !== 'function') throw new Error('Function "' + P.fn + '" is not defined');
        const types = P.params.map((x) => x[1]);
        const args = t.in.map((a, i) => convIn(types[i], a));
        const t0 = now();
        let r = fn(...args);
        ms = now() - t0;
        if (P.inplace != null) r = args[P.inplace];
        if (P.post) {
          const pre = args[0].slice(0, r);
          out = [r, P.post === 'prefix_sorted' ? pre.sort((a, b) => a - b) : pre];
        } else out = convOut(P.ret, r);
      } else if (P.kind === 'design') {
        const { ops, args } = t.in;
        let obj = null; const res = [];
        const t0 = now();
        for (let i = 0; i < ops.length; i++) {
          let a;
          if (i === 0) {
            const ctorT = ((P.design || {}).ctor || []).map((x) => x[1]);
            a = args[0].map((x, k) => convIn(ctorT[k], x));
          } else a = clone(args[i]);
          if (i === 0) {
            const C = lookup(ops[0]);
            if (typeof C !== 'function') throw new Error('Class "' + ops[0] + '" is not defined');
            obj = new C(...a); res.push(null);
          } else {
            if (typeof obj[ops[i]] !== 'function') throw new Error('Method "' + ops[i] + '" is not defined');
            const r = obj[ops[i]](...a); res.push(r === undefined ? null : r);
          }
        }
        ms = now() - t0; out = res;
      } else {
        const rt = P.rt; const C = lookup(rt.cls);
        if (typeof C !== 'function') throw new Error('Class "' + rt.cls + '" is not defined');
        const t0 = now();
        const c = new C();
        const data = c[rt.enc](rt.type === 'TreeNode' ? mkTree(t.in) : clone(t.in));
        if (typeof data !== 'string') throw new Error('encode/serialize must return a string, got ' + typeof data);
        const c2 = new C();
        const back = c2[rt.dec](data);
        ms = now() - t0;
        out = rt.type === 'TreeNode' ? treeOut(back) : (back === undefined ? null : back);
      }
      emit({ i: idx, ok: true, out, ms: Math.round(ms * 1000) / 1000 });
    } catch (e) {
      emit({ i: idx, ok: false, err: fmtErr(e) });
    }
  }
  fs.closeSync(fd);
}
