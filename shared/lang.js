// Shared between the Electron main process (runner) and the renderer (starter code, language menu).
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.Lang = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const LANGS = [
    { id: 'python', label: 'Python3', monaco: 'python', ext: 'py' },
    { id: 'javascript', label: 'JavaScript', monaco: 'javascript', ext: 'js' },
    { id: 'java', label: 'Java', monaco: 'java', ext: 'java' },
    { id: 'cpp', label: 'C++', monaco: 'cpp', ext: 'cpp' },
  ];

  // Types that Java / C++ harnesses can read and write.
  const SIMPLE = new Set(['int', 'long', 'bool', 'string', 'double', 'int[]', 'string[]', 'int[][]', 'char[][]', 'string[][]', 'void']);

  function supports(p, lang) {
    if (lang === 'python' || lang === 'javascript') return true;
    if (p.kind !== 'func' || p.post) return false;
    return p.params.every((x) => SIMPLE.has(x[1])) && SIMPLE.has(p.ret);
  }

  const PY = {
    int: 'int', long: 'int', bool: 'bool', string: 'str', double: 'float', char: 'str', void: 'None',
    'int[]': 'List[int]', 'string[]': 'List[str]', 'int[][]': 'List[List[int]]',
    'char[][]': 'List[List[str]]', 'string[][]': 'List[List[str]]',
    ListNode: 'Optional[ListNode]', 'ListNode[]': 'List[Optional[ListNode]]', TreeNode: 'Optional[TreeNode]',
    Node: "'Optional[Node]'", RandomList: "'Optional[Node]'", CycleList: 'Optional[ListNode]', NextTree: "'Optional[Node]'", QuadTree: "'Node'",
    'double[]': 'List[float]', 'bool[]': 'List[bool]',
  };
  const JS = {
    int: 'number', long: 'number', bool: 'boolean', string: 'string', double: 'number', char: 'character', void: 'void',
    'int[]': 'number[]', 'string[]': 'string[]', 'int[][]': 'number[][]', 'char[][]': 'character[][]',
    'string[][]': 'string[][]', ListNode: 'ListNode', 'ListNode[]': 'ListNode[]', TreeNode: 'TreeNode',
    Node: '_Node', RandomList: '_Node', CycleList: 'ListNode', NextTree: 'Node', QuadTree: 'Node', 'double[]': 'number[]', 'bool[]': 'boolean[]',
  };
  const JAVA = {
    int: 'int', long: 'long', bool: 'boolean', string: 'String', double: 'double', void: 'void',
    'int[]': 'int[]', 'string[]': 'String[]', 'int[][]': 'int[][]', 'char[][]': 'char[][]', 'string[][]': 'String[][]',
  };
  const CPP = {
    int: 'int', long: 'long long', bool: 'bool', string: 'string', double: 'double', void: 'void',
    'int[]': 'vector<int>', 'string[]': 'vector<string>', 'int[][]': 'vector<vector<int>>',
    'char[][]': 'vector<vector<char>>', 'string[][]': 'vector<vector<string>>',
  };

  const PY_NOTES = {
    ListNode: '# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\n',
    TreeNode: '# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\n',
    Node: '# Definition for a Node.\n# class Node:\n#     def __init__(self, val = 0, neighbors = None):\n#         self.val = val\n#         self.neighbors = neighbors if neighbors is not None else []\n',
    RandomList: '# Definition for a Node.\n# class Node:\n#     def __init__(self, x: int, next: \'Node\' = None, random: \'Node\' = None):\n#         self.val = int(x)\n#         self.next = next\n#         self.random = random\n',
  };
  PY_NOTES.NextTree = '# Definition for a Node.\n# class Node:\n#     def __init__(self, val: int = 0, left: \'Node\' = None, right: \'Node\' = None, next: \'Node\' = None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\n#         self.next = next\n';
  PY_NOTES.QuadTree = '# Definition for a QuadTree node.\n# class Node:\n#     def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight):\n#         self.val = val\n#         self.isLeaf = isLeaf\n#         self.topLeft = topLeft\n#         self.topRight = topRight\n#         self.bottomLeft = bottomLeft\n#         self.bottomRight = bottomRight\n';
  const JS_NOTES = {
    ListNode: '/**\n * Definition for singly-linked list.\n * function ListNode(val, next) {\n *     this.val = (val===undefined ? 0 : val)\n *     this.next = (next===undefined ? null : next)\n * }\n */\n',
    TreeNode: '/**\n * Definition for a binary tree node.\n * function TreeNode(val, left, right) {\n *     this.val = (val===undefined ? 0 : val)\n *     this.left = (left===undefined ? null : left)\n *     this.right = (right===undefined ? null : right)\n * }\n */\n',
    Node: '/**\n * // Definition for a _Node.\n * function _Node(val, neighbors) {\n *    this.val = val === undefined ? 0 : val;\n *    this.neighbors = neighbors === undefined ? [] : neighbors;\n * };\n */\n',
    RandomList: '/**\n * // Definition for a _Node.\n * function _Node(val, next, random) {\n *    this.val = val;\n *    this.next = next;\n *    this.random = random;\n * };\n */\n',
  };

  JS_NOTES.NextTree = '/**\n * // Definition for a _Node.\n * function Node(val, left, right, next) {\n *    this.val = val === undefined ? null : val;\n *    this.left = left === undefined ? null : left;\n *    this.right = right === undefined ? null : right;\n *    this.next = next === undefined ? null : next;\n * };\n */\n';
  JS_NOTES.QuadTree = '/**\n * // Definition for a QuadTree node.\n * function Node(val, isLeaf, topLeft, topRight, bottomLeft, bottomRight) {\n *    this.val = val;\n *    this.isLeaf = isLeaf;\n *    this.topLeft = topLeft;\n *    this.topRight = topRight;\n *    this.bottomLeft = bottomLeft;\n *    this.bottomRight = bottomRight;\n * };\n */\n';

  function pyType(t) { return PY[t] || 'Any'; }
  function jsType(t) { return JS[t] || '*'; }

  function pythonStarter(p) {
    if (p.kind === 'design' || p.kind === 'roundtrip') {
      const d = p.design || p.rt;
      let s = 'class ' + d.cls + ':\n\n    def __init__(self' + (d.ctor || []).map((x) => ', ' + x[0] + ': ' + pyType(x[1])).join('') + '):\n        pass\n';
      for (const m of d.methods) {
        s += '\n    def ' + m[0] + '(self' + m[1].map((x) => ', ' + x[0] + ': ' + pyType(x[1])).join('') + ') -> ' + pyType(m[2]) + ':\n        pass\n';
      }
      if (p.kind === 'roundtrip') {
        const t = d.type;
        const note = PY_NOTES[t] || '';
        s = note + (note ? '\n' : '') + s;
      }
      return s;
    }
    const seen = new Set();
    let notes = '';
    for (const t of [...p.params.map((x) => x[1]), p.ret]) {
      const base = t.replace('[]', '');
      if (PY_NOTES[base] && !seen.has(base)) { seen.add(base); notes += PY_NOTES[base]; }
    }
    return (notes ? notes : '') + 'class Solution:\n    def ' + p.fn + '(self' +
      p.params.map((x) => ', ' + x[0] + ': ' + pyType(x[1])).join('') + ') -> ' + (p.inplace != null ? 'None' : pyType(p.ret)) + ':\n        ' +
      (p.inplace != null ? '"""Do not return anything, modify in-place instead."""\n        ' : '') + 'pass\n';
  }

  function jsDoc(params, ret, inplace) {
    let s = '/**\n';
    for (const x of params) s += ' * @param {' + jsType(x[1]) + '} ' + x[0] + '\n';
    s += ' * @return {' + (inplace != null ? 'void' : jsType(ret)) + '}\n */\n';
    return s;
  }

  function javascriptStarter(p) {
    if (p.kind === 'design' || p.kind === 'roundtrip') {
      const d = p.design || p.rt;
      let s = '';
      if (p.kind === 'roundtrip' && JS_NOTES[d.type]) s += JS_NOTES[d.type];
      s += '/**\n' + (d.ctor || []).map((x) => ' * @param {' + jsType(x[1]) + '} ' + x[0] + '\n').join('') + ' */\n';
      s += 'var ' + d.cls + ' = function(' + (d.ctor || []).map((x) => x[0]).join(', ') + ') {\n    \n};\n';
      for (const m of d.methods) {
        s += '\n' + jsDoc(m[1], m[2], null) + d.cls + '.prototype.' + m[0] + ' = function(' + m[1].map((x) => x[0]).join(', ') + ') {\n    \n};\n';
      }
      return s;
    }
    const seen = new Set();
    let notes = '';
    for (const t of [...p.params.map((x) => x[1]), p.ret]) {
      const base = t.replace('[]', '');
      if (JS_NOTES[base] && !seen.has(base)) { seen.add(base); notes += JS_NOTES[base]; }
    }
    return notes + jsDoc(p.params, p.ret, p.inplace) + 'var ' + p.fn + ' = function(' + p.params.map((x) => x[0]).join(', ') + ') {\n    \n};\n';
  }

  function javaStarter(p) {
    return 'class Solution {\n    public ' + (p.inplace != null ? 'void' : JAVA[p.ret]) + ' ' + p.fn + '(' +
      p.params.map((x) => JAVA[x[1]] + ' ' + x[0]).join(', ') + ') {\n        \n    }\n}\n';
  }

  function cppStarter(p) {
    const ref = (t) => (t.endsWith('[]') ? CPP[t] + '&' : CPP[t]);
    return 'class Solution {\npublic:\n    ' + (p.inplace != null ? 'void' : CPP[p.ret]) + ' ' + p.fn + '(' +
      p.params.map((x) => ref(x[1]) + ' ' + x[0]).join(', ') + ') {\n        \n    }\n};\n';
  }

  function starter(p, lang) {
    if (lang === 'python') return pythonStarter(p);
    if (lang === 'javascript') return javascriptStarter(p);
    if (lang === 'java') return javaStarter(p);
    return cppStarter(p);
  }

  return { LANGS, SIMPLE, supports, starter, JAVA, CPP };
});
