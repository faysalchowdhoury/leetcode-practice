# Test harness for Python submissions.
# Reads input.json + solution.py from the working directory and appends one JSON line per test to results.jsonl.
import sys, os, json, time, traceback, copy, threading
import collections, heapq, bisect, math, itertools, functools, string, re, random
from typing import *
from collections import defaultdict, deque, Counter, OrderedDict
from heapq import heappush, heappop, heapify, heappushpop, heapreplace, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort, insort_left, insort_right, bisect
from functools import lru_cache, cache, reduce, cmp_to_key
from itertools import accumulate, combinations, permutations, product, chain, zip_longest, groupby
from math import inf, gcd, sqrt, ceil, floor, log2, comb, factorial

RESULTS = None
EMIT_HOOK = None  # set by the browser (Pyodide) runner


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


GraphNode.__name__ = 'Node'


class RandNode:
    def __init__(self, x: int = 0, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random


RandNode.__name__ = 'Node'

class NextNode:
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


NextNode.__name__ = 'Node'


class QNode:
    def __init__(self, val=False, isLeaf=False, topLeft=None, topRight=None, bottomLeft=None, bottomRight=None):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


QNode.__name__ = 'Node'

CTX = {'orig': set()}


def mk_list(a):
    d = ListNode(0)
    c = d
    for v in a:
        c.next = ListNode(v)
        c = c.next
    return d.next


def list_out(h):
    r = []
    n = 0
    while h is not None:
        r.append(h.val)
        h = h.next
        n += 1
        if n > 2_000_000:
            raise ValueError('The returned linked list seems to contain a cycle')
    return r


def mk_cycle(a):
    vals, pos = a
    head = mk_list(vals)
    if pos >= 0 and head is not None:
        target = head
        for _ in range(pos):
            target = target.next
        tail = head
        while tail.next is not None:
            tail = tail.next
        tail.next = target
    return head


def mk_tree(a, cls=None):
    cls = cls or TreeNode
    if not a or a[0] is None:
        return None
    root = cls(a[0])
    q = deque([root])
    i = 1
    while q and i < len(a):
        n = q.popleft()
        if i < len(a) and a[i] is not None:
            n.left = cls(a[i])
            q.append(n.left)
        i += 1
        if i < len(a) and a[i] is not None:
            n.right = cls(a[i])
            q.append(n.right)
        i += 1
    return root


def tree_out(root):
    if root is None:
        return []
    r = []
    q = deque([root])
    while q:
        n = q.popleft()
        if n is None:
            r.append(None)
        else:
            r.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while r and r[-1] is None:
        r.pop()
    return r


def mk_graph(adj):
    if not adj:
        return None
    nodes = [GraphNode(i + 1) for i in range(len(adj))]
    for i, nb in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nb]
    CTX['orig'] = {id(n) for n in nodes}
    return nodes[0]


def graph_out(node):
    if node is None:
        return []
    seen = {id(node): node}
    q = deque([node])
    while q:
        n = q.popleft()
        for m in n.neighbors:
            if id(m) not in seen:
                seen[id(m)] = m
                q.append(m)
    for k in seen:
        if k in CTX['orig']:
            raise ValueError('You returned the original nodes. Build a deep copy of the graph.')
    size = max(n.val for n in seen.values())
    res = [[] for _ in range(size)]
    for n in seen.values():
        res[n.val - 1] = sorted(m.val for m in n.neighbors)
    return res


def mk_rand(a):
    if not a:
        return None
    nodes = [RandNode(v) for v, _ in a]
    for i, n in enumerate(nodes):
        if i + 1 < len(nodes):
            n.next = nodes[i + 1]
        if a[i][1] is not None:
            n.random = nodes[a[i][1]]
    CTX['orig'] = {id(n) for n in nodes}
    return nodes[0]


def rand_out(head):
    nodes = []
    idx = {}
    n = head
    while n is not None:
        if id(n) in idx:
            raise ValueError('The returned list contains a cycle')
        if id(n) in CTX['orig']:
            raise ValueError('You returned original nodes. Build a deep copy of the list.')
        idx[id(n)] = len(nodes)
        nodes.append(n)
        n = n.next
    out = []
    for n in nodes:
        if n.random is None:
            out.append([n.val, None])
        else:
            if id(n.random) not in idx:
                raise ValueError('A random pointer points outside the returned list')
            out.append([n.val, idx[id(n.random)]])
    return out


def next_out(root):
    levels = []
    if root is None:
        return levels
    level = [root]
    while level:
        for i, n in enumerate(level):
            want = level[i + 1] if i + 1 < len(level) else None
            if n.next is not want:
                raise ValueError('The next pointer of node %s is wrong (it should point to %s)' % (n.val, 'null' if want is None else want.val))
        levels.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c is not None]
    return levels


def quad_out(root):
    out = []
    q = deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append(None)
            continue
        out.append([1 if n.isLeaf else 0, (1 if n.val else 0) if n.isLeaf else 1])
        if not n.isLeaf:
            q.extend([n.topLeft, n.topRight, n.bottomLeft, n.bottomRight])
    while out and out[-1] is None:
        out.pop()
    return out


def norm(v):
    if isinstance(v, tuple):
        return [norm(x) for x in v]
    if isinstance(v, list):
        return [norm(x) for x in v]
    return v


def conv_in(t, v):
    if t == 'ListNode':
        return mk_list(v)
    if t == 'ListNode[]':
        return [mk_list(x) for x in v]
    if t == 'TreeNode':
        return mk_tree(v)
    if t == 'Node':
        return mk_graph(v)
    if t == 'RandomList':
        return mk_rand(v)
    if t == 'CycleList':
        return mk_cycle(v)
    if t == 'NextTree':
        return mk_tree(v, NextNode)
    return copy.deepcopy(v)


def conv_out(t, v):
    if t == 'ListNode':
        return list_out(v)
    if t == 'TreeNode':
        return tree_out(v)
    if t == 'Node':
        return graph_out(v)
    if t == 'RandomList':
        return rand_out(v)
    if t == 'NextTree':
        return next_out(v)
    if t == 'QuadTree':
        return quad_out(v)
    return norm(v)


def fmt_exc(e):
    tb = traceback.extract_tb(e.__traceback__)
    frames = [f for f in tb if f.filename == 'solution.py']
    lines = ['Traceback (most recent call last):']
    for f in frames[-6:]:
        lines.append('  Line %d, in %s' % (f.lineno, f.name))
        if f.line:
            lines.append('    ' + f.line.strip())
    lines += [x.rstrip('\n') for x in traceback.format_exception_only(type(e), e)]
    return '\n'.join(lines)


def emit(rec):
    s = json.dumps(rec)
    if EMIT_HOOK is not None:
        EMIT_HOOK(s)
        return
    RESULTS.write(s + '\n')
    RESULTS.flush()


def run_func(P, ns, args):
    types = [x[1] for x in P['params']]
    conv = [conv_in(t, a) for t, a in zip(types, args)]
    sol = ns['Solution']()
    fn = getattr(sol, P['fn'])
    t0 = time.perf_counter()
    r = fn(*conv)
    ms = (time.perf_counter() - t0) * 1000
    if P.get('inplace') is not None:
        r = conv[P['inplace']]
    post = P.get('post')
    if post:
        pre = list(conv[0][:r])
        return [r, sorted(pre) if post == 'prefix_sorted' else pre], ms
    return conv_out(P['ret'], r), ms


def run_design(P, ns, test):
    ops, args = test['ops'], test['args']
    obj = None
    res = []
    t0 = time.perf_counter()
    for i, (op, a) in enumerate(zip(ops, args)):
        if i == 0:
            ctor = (P.get('design') or {}).get('ctor') or []
            a = [conv_in(c[1], x) for c, x in zip(ctor, a)]
        else:
            a = copy.deepcopy(a)
        if i == 0:
            obj = ns[op](*a)
            res.append(None)
        else:
            res.append(norm(getattr(obj, op)(*a)))
    return res, (time.perf_counter() - t0) * 1000


def run_roundtrip(P, ns, inp):
    rt = P['rt']
    typ = rt['type']
    t0 = time.perf_counter()
    c = ns[rt['cls']]()
    if typ == 'TreeNode':
        data = getattr(c, rt['enc'])(mk_tree(inp))
        c2 = ns[rt['cls']]()
        res = tree_out(getattr(c2, rt['dec'])(data))
    else:
        data = getattr(c, rt['enc'])(copy.deepcopy(inp))
        if not isinstance(data, str):
            raise TypeError('encode/serialize must return a string, got ' + type(data).__name__)
        c2 = ns[rt['cls']]()
        res = norm(getattr(c2, rt['dec'])(data))
    return res, (time.perf_counter() - t0) * 1000


def main():
    global RESULTS
    cfg = json.load(open('input.json', encoding='utf-8'))
    P = cfg['problem']
    tests = cfg['tests']
    if EMIT_HOOK is None:
        RESULTS = open('results.jsonl', 'w', encoding='utf-8')
    code = open('solution.py', encoding='utf-8').read()
    ns = {k: v for k, v in globals().items() if not k.startswith('__')}
    ns['__name__'] = 'solution'
    ns['ListNode'] = ListNode
    ns['TreeNode'] = TreeNode
    ptypes = [x[1] for x in (P.get('params') or [])]
    if 'Node' in ptypes:
        ns['Node'] = GraphNode
    elif 'NextTree' in ptypes:
        ns['Node'] = NextNode
    elif P.get('ret') == 'QuadTree':
        ns['Node'] = QNode
    else:
        ns['Node'] = RandNode
    try:
        exec(compile(code, 'solution.py', 'exec'), ns)
    except SyntaxError as e:
        emit({'fatal': 'SyntaxError: %s (line %s)' % (e.msg, e.lineno), 'syntax': True})
        return
    except BaseException as e:
        emit({'fatal': fmt_exc(e)})
        return

    for idx, t in enumerate(tests):
        try:
            kind = P['kind']
            if kind == 'func':
                out, ms = run_func(P, ns, t['in'])
            elif kind == 'design':
                out, ms = run_design(P, ns, t['in'])
            else:
                out, ms = run_roundtrip(P, ns, t['in'])
            try:
                line = {'i': idx, 'ok': True, 'out': out, 'ms': round(ms, 3)}
                json.dumps(line)
            except (TypeError, ValueError):
                line = {'i': idx, 'ok': False, 'err': 'Your output is not a plain value (got %s). Return lists / numbers / strings.' % type(out).__name__}
            emit(line)
        except BaseException as e:
            emit({'i': idx, 'ok': False, 'err': fmt_exc(e)})


if __name__ == '__main__' and sys.platform == 'emscripten':
    sys.setrecursionlimit(5000)
    main()
elif __name__ == '__main__':
    sys.setrecursionlimit(200000)
    for size in (512, 256, 128, 64):
        try:
            threading.stack_size(size * 1024 * 1024)
            break
        except (ValueError, RuntimeError):
            continue
    th = threading.Thread(target=main)
    th.start()
    th.join()
