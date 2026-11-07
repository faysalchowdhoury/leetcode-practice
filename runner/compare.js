// Result comparison modes. Used by the runner (main process).
'use strict';

function canon(v) {
  return JSON.stringify(v === undefined ? null : v);
}

function deepEqual(a, b) {
  return canon(a) === canon(b);
}

function sortedFlat(a) {
  if (!Array.isArray(a)) return a;
  return a.slice().sort((x, y) => (canon(x) < canon(y) ? -1 : canon(x) > canon(y) ? 1 : 0));
}

function sortedDeep(a) {
  if (!Array.isArray(a)) return a;
  const inner = a.map((x) => (Array.isArray(x) ? sortedFlat(x) : x));
  return sortedFlat(inner);
}

function checkTopo(actual, expected, input) {
  const n = input[0];
  const pre = input[1];
  if (Array.isArray(expected) && expected.length === 0) return Array.isArray(actual) && actual.length === 0;
  if (!Array.isArray(actual) || actual.length !== n) return false;
  const pos = new Map();
  actual.forEach((c, i) => pos.set(c, i));
  if (pos.size !== n) return false;
  for (let c = 0; c < n; c++) if (!pos.has(c)) return false;
  return pre.every(([a, b]) => pos.get(b) < pos.get(a));
}

function checkAlien(actual, expected, input) {
  const words = input[0];
  if (expected === '') return actual === '';
  if (typeof actual !== 'string') return false;
  const chars = new Set(words.join('').split(''));
  if (new Set(actual.split('')).size !== actual.length) return false;
  if (actual.length !== chars.size) return false;
  for (const c of chars) if (!actual.includes(c)) return false;
  for (let i = 0; i + 1 < words.length; i++) {
    const a = words[i], b = words[i + 1];
    const m = Math.min(a.length, b.length);
    let j = 0;
    while (j < m && a[j] === b[j]) j++;
    if (j < m && actual.indexOf(a[j]) > actual.indexOf(b[j])) return false;
  }
  return true;
}

function checkPalSub(actual, expected, input) {
  const s = input[0];
  if (typeof actual !== 'string' || actual.length !== expected.length) return false;
  if (!s.includes(actual)) return false;
  return actual === actual.split('').reverse().join('');
}

function checkPeak(actual, expected, input) {
  const a = input[0];
  if (!Number.isInteger(actual) || actual < 0 || actual >= a.length) return false;
  const l = actual > 0 ? a[actual - 1] : -Infinity;
  const r = actual + 1 < a.length ? a[actual + 1] : -Infinity;
  return a[actual] > l && a[actual] > r;
}

function checkKPairs(actual, expected, input) {
  const [n1, n2] = input;
  if (!Array.isArray(actual) || actual.length !== expected.length) return false;
  if (!actual.every((p) => Array.isArray(p) && p.length === 2 && n1.includes(p[0]) && n2.includes(p[1]))) return false;
  const sums = (arr) => arr.map((p) => p[0] + p[1]).sort((x, y) => x - y).join(',');
  return sums(actual) === sums(expected);
}

function checkBstBalanced(actual, expected, input) {
  const nums = input[0];
  if (!Array.isArray(actual)) return false;
  if (!nums.length) return actual.length === 0;
  const nodes = []; const root = { v: actual[0], l: null, r: null };
  if (actual[0] === null) return false;
  const q = [root]; let h = 0, i = 1;
  while (h < q.length && i < actual.length) {
    const n = q[h++];
    if (i < actual.length && actual[i] !== null) { n.l = { v: actual[i], l: null, r: null }; q.push(n.l); } i++;
    if (i < actual.length && actual[i] !== null) { n.r = { v: actual[i], l: null, r: null }; q.push(n.r); } i++;
  }
  const inorder = []; let ok = true;
  const height = (n) => {
    if (!n) return 0;
    const lh = height(n.l); const rh = height(n.r);
    if (Math.abs(lh - rh) > 1) ok = false;
    return 1 + Math.max(lh, rh);
  };
  const walk = (n) => { if (!n) return; walk(n.l); inorder.push(n.v); walk(n.r); };
  walk(root); height(root);
  return ok && deepEqual(inorder, nums);
}

function compare(mode, actual, expected, input) {
  switch (mode) {
    case 'sorted': return deepEqual(sortedFlat(actual), sortedFlat(expected));
    case 'sorted_deep': return deepEqual(sortedDeep(actual), sortedDeep(expected));
    case 'float':
      return typeof actual === 'number' && Math.abs(actual - expected) <= 1e-5 * Math.max(1, Math.abs(expected));
    case 'topo': return checkTopo(actual, expected, input);
    case 'alien': return checkAlien(actual, expected, input);
    case 'palsub': return checkPalSub(actual, expected, input);
    case 'peak': return checkPeak(actual, expected, input);
    case 'kpairs': return checkKPairs(actual, expected, input);
    case 'bst_bal': return checkBstBalanced(actual, expected, input);
    case 'float_arr':
      return Array.isArray(actual) && actual.length === expected.length && actual.every((x, i) => typeof x === 'number' && Math.abs(x - expected[i]) <= 1e-5 * Math.max(1, Math.abs(expected[i])));
    default: return deepEqual(actual, expected);
  }
}

module.exports = { compare };
