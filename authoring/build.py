#!/usr/bin/env python3
"""Builds renderer/problems-data.js.

For every problem the reference solution is executed through runner/harness.py (the exact harness the app uses for
Python submissions) to produce the expected outputs, so expected values are never typed by hand.
"""
import json, os, subprocess, sys, tempfile, shutil, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import groups  # noqa: E402


def run_ref(p):
    tmp = tempfile.mkdtemp(prefix='lcbuild-')
    try:
        shutil.copy(os.path.join(ROOT, 'runner', 'harness.py'), tmp)
        open(os.path.join(tmp, 'solution.py'), 'w').write(p['ref'])
        slim = {k: p.get(k) for k in ('kind', 'fn', 'params', 'ret', 'inplace', 'design', 'rt', 'post')}
        json.dump({'problem': slim, 'tests': p['tests']}, open(os.path.join(tmp, 'input.json'), 'w'))
        r = subprocess.run([sys.executable, 'harness.py'], cwd=tmp, capture_output=True, text=True, timeout=120)
        recs = {}
        for line in open(os.path.join(tmp, 'results.jsonl')):
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if 'fatal' in d:
                raise RuntimeError('reference failed to load: ' + d['fatal'])
            recs[d['i']] = d
        out = []
        for i in range(len(p['tests'])):
            d = recs.get(i)
            if d is None or not d['ok']:
                raise RuntimeError('reference failed on test %d: %s' % (i, (d or {}).get('err', r.stderr[-400:])))
            out.append(d['out'])
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    problems = []
    group_list = []
    pid = 0
    failures = 0
    for gi, g in enumerate(groups.GROUPS):
        ids = []
        for p in g['problems']:
            pid += 1
            try:
                outs = run_ref(p)
            except Exception as e:  # keep going so every failure is reported at once
                failures += 1
                print('FAIL  #%d %s: %s' % (pid, p['title'], e))
                continue
            for t, o in zip(p['tests'], outs):
                t['expected'] = o
            q = {k: v for k, v in p.items() if k != 'ref'}
            q['id'] = pid
            q['group'] = gi
            problems.append(q)
            ids.append(pid)
        group_list.append({'index': gi, 'name': g['name'], 'tip': g.get('tip', ''), 'ids': ids})
    if failures:
        print('\n%d problem(s) failed' % failures)
        sys.exit(1)
    out_path = os.path.join(ROOT, 'renderer', 'problems-data.js')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('window.GROUPS = ' + json.dumps(group_list, ensure_ascii=False) + ';\n')
        f.write('window.PROBLEMS = ' + json.dumps(problems, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print('OK: %d groups, %d problems, %.1f KB -> %s' % (len(group_list), len(problems), os.path.getsize(out_path) / 1024, out_path))


if __name__ == '__main__':
    main()
