"""Tiny DSL used to author problems. Expected outputs are NOT written by hand:
build.py runs each reference solution through the same harness the app uses and records the output."""
import re
from textwrap import dedent


def _params(s):
    out = []
    for part in [x.strip() for x in s.split(',') if x.strip()]:
        n, t = part.split(':')
        out.append([n.strip(), t.strip()])
    return out


def F(title, lc, diff, desc, sig, tests, ref, cmp='exact', inplace=None, hint=None, ex=2, post=None):
    """Function problem. sig = 'name(a:int[], b:int)->int'. tests = list of argument tuples."""
    m = re.match(r'(\w+)\((.*)\)->(\S+)$', sig)
    fn, ps, ret = m.group(1), m.group(2), m.group(3)
    params = _params(ps)
    ip = None
    if inplace:
        ip = [p[0] for p in params].index(inplace)
        ret = params[ip][1]
    return dict(kind='func', title=title, lc=lc, diff=diff, desc=dedent(desc).strip(), fn=fn, params=params, ret=ret,
                inplace=ip, cmp=cmp, post=post, tests=[{'in': list(t)} for t in tests], ref=dedent(ref).strip() + '\n', hint=hint, ex=ex)


def _method(s):
    m = re.match(r'(\w+)\((.*)\)->(\S+)$', s)
    return [m.group(1), _params(m.group(2)), m.group(3)]


def D(title, lc, diff, desc, cls, ctor, methods, tests, ref, hint=None, ex=1):
    """Class-design problem. tests = list of call lists: [("Cls",[args]),("method",[args]),...]."""
    t = []
    for calls in tests:
        assert calls[0][0] == cls, title
        t.append({'in': {'ops': [c[0] for c in calls], 'args': [c[1] for c in calls]}})
    return dict(kind='design', title=title, lc=lc, diff=diff, desc=dedent(desc).strip(), design={'cls': cls, 'ctor': _params(ctor), 'methods': [_method(x) for x in methods]},
                cmp='exact', tests=t, ref=dedent(ref).strip() + '\n', hint=hint, ex=ex)


def R(title, lc, diff, desc, cls, enc, dec, typ, tests, ref, hint=None, ex=2):
    """Round-trip problem: decode(encode(x)) must give x back."""
    sig_in = 'root' if typ == 'TreeNode' else 'strs'
    sig_out = 'TreeNode' if typ == 'TreeNode' else 'string[]'
    methods = [[enc, [[sig_in, typ]], 'string'], [dec, [['data', 'string']], sig_out]]
    return dict(kind='roundtrip', title=title, lc=lc, diff=diff, desc=dedent(desc).strip(), rt={'cls': cls, 'enc': enc, 'dec': dec, 'type': typ, 'methods': methods, 'ctor': []},
                cmp='exact', tests=[{'in': x} for x in tests], ref=dedent(ref).strip() + '\n', hint=hint, ex=ex)
