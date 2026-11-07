// Text encoding of test data and source generation for the Java and C++ harnesses.
'use strict';
const Lang = require('../shared/lang');

const SUF = { int: 'i', long: 'L', bool: 'b', string: 's', double: 'd', 'int[]': 'iA', 'string[]': 'sA', 'int[][]': 'iAA', 'char[][]': 'cAA', 'string[][]': 'sAA' };

// ---- value <-> lines (one token per line) ----
function enc(type, v, out) {
  switch (type) {
    case 'int': case 'long': case 'double': out.push(String(v)); break;
    case 'bool': out.push(v ? 'true' : 'false'); break;
    case 'string': out.push(String(v)); break;
    case 'int[]': case 'string[]':
      out.push(String(v.length)); for (const x of v) out.push(String(x)); break;
    case 'int[][]': case 'char[][]': case 'string[][]':
      out.push(String(v.length));
      for (const row of v) { out.push(String(row.length)); for (const x of row) out.push(String(x)); }
      break;
    default: throw new Error('Unsupported type ' + type);
  }
}

function dec(type, lines, cur) {
  const next = () => (cur.i < lines.length ? lines[cur.i++] : '');
  switch (type) {
    case 'int': case 'long': return parseInt(next(), 10);
    case 'double': return parseFloat(next());
    case 'bool': return next().trim() === 'true';
    case 'string': return next();
    case 'int[]': { const n = parseInt(next(), 10); const a = []; for (let k = 0; k < n; k++) a.push(parseInt(next(), 10)); return a; }
    case 'string[]': { const n = parseInt(next(), 10); const a = []; for (let k = 0; k < n; k++) a.push(next()); return a; }
    case 'int[][]': { const n = parseInt(next(), 10); const a = []; for (let r = 0; r < n; r++) { const m = parseInt(next(), 10); const row = []; for (let k = 0; k < m; k++) row.push(parseInt(next(), 10)); a.push(row); } return a; }
    case 'char[][]': case 'string[][]': { const n = parseInt(next(), 10); const a = []; for (let r = 0; r < n; r++) { const m = parseInt(next(), 10); const row = []; for (let k = 0; k < m; k++) row.push(next()); a.push(row); } return a; }
    default: throw new Error('Unsupported type ' + type);
  }
}

function encodeInput(p, tests) {
  const out = [String(tests.length)];
  for (const t of tests) p.params.forEach((x, i) => enc(x[1], t.in[i], out));
  return out.join('\n') + '\n';
}

function parseResults(p, text) {
  const lines = text.split('\n').map((l) => l.replace(/\r$/, ''));
  const recs = {};
  let i = 0;
  while (i < lines.length) {
    const l = lines[i];
    if (l.startsWith('@@T ')) {
      const parts = l.split(' ');
      const idx = parseInt(parts[1], 10);
      const ms = parseFloat(parts[2]);
      const body = [];
      i++;
      while (i < lines.length && lines[i] !== '@@E') body.push(lines[i++]);
      if (i >= lines.length) break; // truncated record (crash while writing)
      try { recs[idx] = { i: idx, ok: true, out: dec(p.ret, body, { i: 0 }), ms }; } catch (e) { recs[idx] = { i: idx, ok: false, err: 'Could not read output' }; }
    } else if (l.startsWith('@@X ')) {
      const idx = parseInt(l.split(' ')[1], 10);
      const body = [];
      i++;
      while (i < lines.length && lines[i] !== '@@E') body.push(lines[i++]);
      recs[idx] = { i: idx, ok: false, err: body.join('\n') };
    }
    i++;
  }
  return recs;
}

// ---- Java ----
function javaHelpers() {
  return `
    static BufferedReader br;
    static PrintWriter out;
    static String rl() throws IOException { String s = br.readLine(); return s == null ? "" : s; }
    static int ri() throws IOException { return Integer.parseInt(rl().trim()); }
    static long rL() throws IOException { return Long.parseLong(rl().trim()); }
    static double rd() throws IOException { return Double.parseDouble(rl().trim()); }
    static boolean rb() throws IOException { return rl().trim().equals("true"); }
    static String rs() throws IOException { return rl(); }
    static int[] riA() throws IOException { int n = ri(); int[] a = new int[n]; for (int i = 0; i < n; i++) a[i] = ri(); return a; }
    static String[] rsA() throws IOException { int n = ri(); String[] a = new String[n]; for (int i = 0; i < n; i++) a[i] = rl(); return a; }
    static int[][] riAA() throws IOException { int n = ri(); int[][] a = new int[n][]; for (int i = 0; i < n; i++) a[i] = riA(); return a; }
    static char[][] rcAA() throws IOException { int n = ri(); char[][] a = new char[n][]; for (int i = 0; i < n; i++) { int m = ri(); a[i] = new char[m]; for (int j = 0; j < m; j++) { String s = rl(); a[i][j] = s.isEmpty() ? ' ' : s.charAt(0); } } return a; }
    static String[][] rsAA() throws IOException { int n = ri(); String[][] a = new String[n][]; for (int i = 0; i < n; i++) a[i] = rsA(); return a; }
    static void wi(int v) { out.println(v); }
    static void wL(long v) { out.println(v); }
    static void wd(double v) { out.println(v); }
    static void wb(boolean v) { out.println(v ? "true" : "false"); }
    static void ws(String v) { out.println(v == null ? "" : v); }
    static void wiA(int[] a) { out.println(a.length); for (int x : a) out.println(x); }
    static void wsA(String[] a) { out.println(a.length); for (String x : a) out.println(x); }
    static void wiAA(int[][] a) { out.println(a.length); for (int[] r : a) wiA(r); }
    static void wcAA(char[][] a) { out.println(a.length); for (char[] r : a) { out.println(r.length); for (char c : r) out.println(c); } }
    static void wsAA(String[][] a) { out.println(a.length); for (String[] r : a) wsA(r); }
`;
}

function genJava(p, userCode) {
  const prelude = 'import java.util.*;import java.io.*;import java.util.stream.*;import java.util.function.*;';
  const decl = p.params.map((x, i) => `${Lang.JAVA[x[1]]} a${i} = r${SUF[x[1]]}();`).join('\n                ');
  const call = `sol.${p.fn}(${p.params.map((_, i) => 'a' + i).join(', ')});`;
  const body = p.inplace != null
    ? `${call}\n                long t1 = System.nanoTime();\n                out.println("@@T " + t + " " + ((t1 - t0) / 1e6));\n                w${SUF[p.ret]}(a${p.inplace});`
    : `${Lang.JAVA[p.ret]} res = ${call}\n                long t1 = System.nanoTime();\n                out.println("@@T " + t + " " + ((t1 - t0) / 1e6));\n                w${SUF[p.ret]}(res);`;
  return `${prelude}${userCode}

public class Main {${javaHelpers()}
    public static void main(String[] args) throws Exception {
        Thread th = new Thread(null, () -> {
            try { run(); } catch (Throwable e) { e.printStackTrace(); }
        }, "runner", 1L << 29);
        th.start();
        th.join();
    }

    static void run() throws Exception {
        br = new BufferedReader(new FileReader("input.txt"));
        out = new PrintWriter(new BufferedWriter(new FileWriter("results.txt")));
        int T = ri();
        for (int t = 0; t < T; t++) {
            try {
                ${decl}
                Solution sol = new Solution();
                long t0 = System.nanoTime();
                ${body}
                out.println("@@E");
            } catch (Throwable e) {
                out.println("@@X " + t);
                out.println(e.toString());
                int shown = 0;
                for (StackTraceElement el : e.getStackTrace()) {
                    if (el.getClassName().startsWith("Solution") && shown++ < 4) out.println("  at line " + el.getLineNumber() + " in " + el.getMethodName());
                }
                out.println("@@E");
            }
            out.flush();
        }
        out.close();
    }
}
`;
}

// ---- C++ ----
function genCpp(p, userCode) {
  const prelude = '#include <iostream>\n#include <fstream>\n#include <sstream>\n#include <vector>\n#include <string>\n#include <unordered_map>\n#include <unordered_set>\n#include <map>\n#include <set>\n#include <queue>\n#include <stack>\n#include <deque>\n#include <list>\n#include <array>\n#include <tuple>\n#include <bitset>\n#include <algorithm>\n#include <numeric>\n#include <functional>\n#include <cmath>\n#include <climits>\n#include <cstring>\n#include <cstdint>\n#include <chrono>\n#include <iomanip>\nusing namespace std;';
  const ref = (t) => Lang.CPP[t];
  const decl = p.params.map((x, i) => `${ref(x[1])} a${i} = r${SUF[x[1]]}();`).join('\n            ');
  const callArgs = p.params.map((_, i) => 'a' + i).join(', ');
  const body = p.inplace != null
    ? `sol.${p.fn}(${callArgs});\n            auto t1 = chrono::steady_clock::now();\n            OUT << "@@T " << t << " " << chrono::duration<double, milli>(t1 - t0).count() << "\\n";\n            w${SUF[p.ret]}(a${p.inplace});`
    : `auto res = sol.${p.fn}(${callArgs});\n            auto t1 = chrono::steady_clock::now();\n            OUT << "@@T " << t << " " << chrono::duration<double, milli>(t1 - t0).count() << "\\n";\n            w${SUF[p.ret]}(res);`;
  const helpers = `
static ifstream IN;
static ofstream OUT;
static string rl() { string s; getline(IN, s); if (!s.empty() && s.back() == '\\r') s.pop_back(); return s; }
static int ri() { return stoi(rl()); }
static long long rL() { return stoll(rl()); }
static double rd() { return stod(rl()); }
static bool rb() { return rl() == "true"; }
static string rs() { return rl(); }
static vector<int> riA() { int n = ri(); vector<int> a(n); for (int i = 0; i < n; i++) a[i] = ri(); return a; }
static vector<string> rsA() { int n = ri(); vector<string> a(n); for (int i = 0; i < n; i++) a[i] = rl(); return a; }
static vector<vector<int>> riAA() { int n = ri(); vector<vector<int>> a(n); for (int i = 0; i < n; i++) a[i] = riA(); return a; }
static vector<vector<char>> rcAA() { int n = ri(); vector<vector<char>> a(n); for (int i = 0; i < n; i++) { int m = ri(); a[i].resize(m); for (int j = 0; j < m; j++) { string s = rl(); a[i][j] = s.empty() ? ' ' : s[0]; } } return a; }
static vector<vector<string>> rsAA() { int n = ri(); vector<vector<string>> a(n); for (int i = 0; i < n; i++) a[i] = rsA(); return a; }
static void wi(int v) { OUT << v << "\\n"; }
static void wL(long long v) { OUT << v << "\\n"; }
static void wd(double v) { OUT << setprecision(12) << v << "\\n"; }
static void wb(bool v) { OUT << (v ? "true" : "false") << "\\n"; }
static void ws(const string& v) { OUT << v << "\\n"; }
static void wiA(const vector<int>& a) { OUT << a.size() << "\\n"; for (int x : a) OUT << x << "\\n"; }
static void wsA(const vector<string>& a) { OUT << a.size() << "\\n"; for (auto& x : a) OUT << x << "\\n"; }
static void wiAA(const vector<vector<int>>& a) { OUT << a.size() << "\\n"; for (auto& r : a) wiA(r); }
static void wcAA(const vector<vector<char>>& a) { OUT << a.size() << "\\n"; for (auto& r : a) { OUT << r.size() << "\\n"; for (char c : r) OUT << c << "\\n"; } }
static void wsAA(const vector<vector<string>>& a) { OUT << a.size() << "\\n"; for (auto& r : a) wsA(r); }
`;
  return `${prelude}
#line 1
${userCode}
${helpers}
int main() {
    IN.open("input.txt");
    OUT.open("results.txt");
    int T = ri();
    for (int t = 0; t < T; t++) {
        try {
            ${decl}
            Solution sol;
            auto t0 = chrono::steady_clock::now();
            ${body}
            OUT << "@@E\\n";
        } catch (const exception& e) {
            OUT << "@@X " << t << "\\n" << "exception: " << e.what() << "\\n@@E\\n";
        } catch (...) {
            OUT << "@@X " << t << "\\n" << "unknown exception\\n@@E\\n";
        }
        OUT.flush();
    }
    return 0;
}
`;
}

module.exports = { encodeInput, parseResults, genJava, genCpp };
