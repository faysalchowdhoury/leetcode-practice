from dsl import F, D, R

N = None
TREE_NOTE = "\n\nIn the tests a binary tree is shown in level order, with `null` for a missing child (for example `[3,9,20,null,null,15,7]`)."

G10 = [
    F("Invert Binary Tree", 226, "Easy", """
        Given the root of a binary tree, invert it (swap the left and right children of every node) and return its root.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 100
        """, "invertTree(root:TreeNode)->TreeNode",
      [([4, 2, 7, 1, 3, 6, 9],), ([2, 1, 3],), ([],), ([1],), ([1, 2],), ([1, N, 2, 3],)],
      """
      class Solution:
          def invertTree(self, root):
              if root:
                  root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
              return root
      """, hint="Recursively swap the children of every node."),
    F("Maximum Depth of Binary Tree", 104, "Easy", """
        Return the maximum depth of a binary tree: the number of nodes along the longest path from the root down to a leaf.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 10^4
        """, "maxDepth(root:TreeNode)->int",
      [([3, 9, 20, N, N, 15, 7],), ([1, N, 2],), ([],), ([1],), ([1, 2, 3, 4, N, N, 5, 6],)],
      """
      class Solution:
          def maxDepth(self, root):
              return 0 if not root else 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
      """, hint="depth(node) = 1 + max(depth(left), depth(right))."),
    F("Diameter of Binary Tree", 543, "Easy", """
        The diameter of a binary tree is the length (in edges) of the longest path between any two nodes. The path may or may not pass through the root. Return the diameter.""" + TREE_NOTE + """

        Constraints:
        - 1 <= number of nodes <= 10^4
        """, "diameterOfBinaryTree(root:TreeNode)->int",
      [([1, 2, 3, 4, 5],), ([1, 2],), ([1],), ([1, 2, 3, 4, 5, N, N, 6, N, N, 7],), ([1, N, 2, N, 3, N, 4],)],
      """
      class Solution:
          def diameterOfBinaryTree(self, root):
              best = 0
              def h(n):
                  nonlocal best
                  if not n:
                      return 0
                  l, r = h(n.left), h(n.right)
                  best = max(best, l + r)
                  return 1 + max(l, r)
              h(root)
              return best
      """, hint="While computing heights, the best path through a node is leftHeight + rightHeight."),
    F("Balanced Binary Tree", 110, "Easy", """
        Return `true` if the tree is height-balanced: for every node, the heights of its left and right subtrees differ by at most 1.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 5000
        """, "isBalanced(root:TreeNode)->bool",
      [([3, 9, 20, N, N, 15, 7],), ([1, 2, 2, 3, 3, N, N, 4, 4],), ([],), ([1, 2, N, 3],), ([1, 2, 3],), ([1, 2, 2, 3, N, N, 3, 4, N, N, 4],)],
      """
      class Solution:
          def isBalanced(self, root):
              def h(n):
                  if not n:
                      return 0
                  l, r = h(n.left), h(n.right)
                  if l < 0 or r < 0 or abs(l - r) > 1:
                      return -1
                  return 1 + max(l, r)
              return h(root) >= 0
      """, hint="Return -1 as a sentinel height as soon as any subtree is unbalanced."),
    F("Same Tree", 100, "Easy", """
        Given the roots of two binary trees `p` and `q`, return `true` if they have the same structure and the same node values.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes in each tree <= 100
        """, "isSameTree(p:TreeNode, q:TreeNode)->bool",
      [([1, 2, 3], [1, 2, 3]), ([1, 2], [1, N, 2]), ([1, 2, 1], [1, 1, 2]), ([], []), ([1], []), ([1, 2, 3, 4], [1, 2, 3, 4])],
      """
      class Solution:
          def isSameTree(self, p, q):
              if not p and not q:
                  return True
              if not p or not q or p.val != q.val:
                  return False
              return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
      """, hint="Compare the roots, then recurse on both children."),
    F("Subtree of Another Tree", 572, "Easy", """
        Return `true` if `subRoot` matches some subtree of `root` exactly (same structure and values, and the subtree includes all descendants of its root).""" + TREE_NOTE + """

        Constraints:
        - 1 <= number of nodes in root <= 2000, 1 <= number of nodes in subRoot <= 1000
        """, "isSubtree(root:TreeNode, subRoot:TreeNode)->bool",
      [([3, 4, 5, 1, 2], [4, 1, 2]), ([3, 4, 5, 1, 2, N, N, N, N, 0], [4, 1, 2]), ([1], [1]), ([1, 1], [1]), ([1, 2, 3], [3]), ([1, 2, 3], [2, 3])],
      """
      class Solution:
          def isSubtree(self, root, subRoot):
              def same(a, b):
                  if not a and not b:
                      return True
                  if not a or not b or a.val != b.val:
                      return False
                  return same(a.left, b.left) and same(a.right, b.right)
              def go(n):
                  return bool(n) and (same(n, subRoot) or go(n.left) or go(n.right))
              return go(root)
      """, hint="At every node of root, test whether the two trees are identical from there."),
    F("Count Good Nodes in Binary Tree", 1448, "Medium", """
        A node is "good" if no node on the path from the root to it has a larger value. Return the number of good nodes. The root is always good.""" + TREE_NOTE + """

        Constraints:
        - 1 <= number of nodes <= 10^5
        - -10^4 <= node value <= 10^4
        """, "goodNodes(root:TreeNode)->int",
      [([3, 1, 4, 3, N, 1, 5],), ([3, 3, N, 4, 2],), ([1],), ([2, N, 4, 10, 8, N, N, 4],), ([9, N, 3, 6],), ([-1, -5, -2, -4, N, -3, -6],)],
      """
      class Solution:
          def goodNodes(self, root):
              def go(n, mx):
                  if not n:
                      return 0
                  return (n.val >= mx) + go(n.left, max(mx, n.val)) + go(n.right, max(mx, n.val))
              return go(root, -10**9)
      """, hint="Pass the maximum value seen on the path down the recursion."),
    F("Binary Tree Maximum Path Sum", 124, "Hard", """
        A path is any sequence of connected nodes in which each node appears at most once; it does not need to pass through the root. Return the maximum sum of node values over all non-empty paths.""" + TREE_NOTE + """

        Constraints:
        - 1 <= number of nodes <= 3 * 10^4
        - -1000 <= node value <= 1000
        """, "maxPathSum(root:TreeNode)->int",
      [([1, 2, 3],), ([-10, 9, 20, N, N, 15, 7],), ([-3],), ([2, -1],), ([5, 4, 8, 11, N, 13, 4, 7, 2, N, N, N, 1],), ([-2, -1],)],
      """
      class Solution:
          def maxPathSum(self, root):
              best = -10**18
              def go(n):
                  nonlocal best
                  if not n:
                      return 0
                  l, r = max(go(n.left), 0), max(go(n.right), 0)
                  best = max(best, n.val + l + r)
                  return n.val + max(l, r)
              go(root)
              return best
      """, hint="Each node returns its best downward path; the best path through it uses both children."),
]

G11 = [
    F("Binary Tree Level Order Traversal", 102, "Medium", """
        Return the level order traversal of a binary tree: a list of lists, where each inner list holds the node values of one depth from left to right.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 2000
        """, "levelOrder(root:TreeNode)->int[][]",
      [([3, 9, 20, N, N, 15, 7],), ([1],), ([],), ([1, 2, 3, 4, 5],), ([1, N, 2, N, 3],)],
      """
      class Solution:
          def levelOrder(self, root):
              if not root:
                  return []
              res = []; q = deque([root])
              while q:
                  res.append([n.val for n in q])
                  for _ in range(len(q)):
                      n = q.popleft()
                      if n.left: q.append(n.left)
                      if n.right: q.append(n.right)
              return res
      """, hint="BFS with a queue; process exactly len(queue) nodes per level."),
    F("Binary Tree Right Side View", 199, "Medium", """
        Imagine standing on the right side of a binary tree. Return the values of the nodes you can see, ordered from top to bottom.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 100
        """, "rightSideView(root:TreeNode)->int[]",
      [([1, 2, 3, N, 5, N, 4],), ([1, N, 3],), ([],), ([1, 2, 3, 4],), ([1, 2, N, 3, N, 4],)],
      """
      class Solution:
          def rightSideView(self, root):
              if not root:
                  return []
              res = []; q = deque([root])
              while q:
                  res.append(q[-1].val)
                  for _ in range(len(q)):
                      n = q.popleft()
                      if n.left: q.append(n.left)
                      if n.right: q.append(n.right)
              return res
      """, hint="The last node of every BFS level is the one visible from the right."),
]

BST = [6, 2, 8, 0, 4, 7, 9, N, N, 3, 5]
BST2 = [5, 3, 8, 2, 4, 7, 9]
G12 = [
    F("Lowest Common Ancestor of a Binary Search Tree", 235, "Medium", """
        Given a binary search tree and two node values `p` and `q` that both exist in it, return the **value** of their lowest common ancestor: the deepest node that has both as descendants (a node counts as a descendant of itself).""" + TREE_NOTE + """

        Constraints:
        - 2 <= number of nodes <= 10^5, all values unique, p != q
        """, "lowestCommonAncestor(root:TreeNode, p:int, q:int)->int",
      [(BST, 2, 8), (BST, 2, 4), ([2, 1], 2, 1), (BST2, 4, 9), (BST2, 7, 9), (BST, 3, 5), (BST, 0, 5)],
      """
      class Solution:
          def lowestCommonAncestor(self, root, p, q):
              n = root
              while n:
                  if p < n.val and q < n.val:
                      n = n.left
                  elif p > n.val and q > n.val:
                      n = n.right
                  else:
                      return n.val
      """, hint="Walk down from the root: if both values are smaller go left, if both larger go right, otherwise you are at the answer."),
    F("Validate Binary Search Tree", 98, "Medium", """
        Return `true` if the tree is a valid BST: every node's left subtree holds only smaller values, its right subtree only larger values, and both subtrees are BSTs.""" + TREE_NOTE + """

        Constraints:
        - 1 <= number of nodes <= 10^4
        """, "isValidBST(root:TreeNode)->bool",
      [([2, 1, 3],), ([5, 1, 4, N, N, 3, 6],), ([1],), ([2, 2, 2],), ([5, 4, 6, N, N, 3, 7],), ([0, -1],), ([3, 1, 5, 0, 2, 4, 6],)],
      """
      class Solution:
          def isValidBST(self, root):
              def ok(n, lo, hi):
                  if not n:
                      return True
                  if not (lo < n.val < hi):
                      return False
                  return ok(n.left, lo, n.val) and ok(n.right, n.val, hi)
              return ok(root, -inf, inf)
      """, hint="Each node must lie strictly between a lower and an upper bound inherited from its ancestors."),
    F("Kth Smallest Element in a BST", 230, "Medium", """
        Return the `k`-th smallest value (1-indexed) among all node values of a BST.""" + TREE_NOTE + """

        Constraints:
        - 1 <= k <= number of nodes <= 10^4
        """, "kthSmallest(root:TreeNode, k:int)->int",
      [([3, 1, 4, N, 2], 1), ([5, 3, 6, 2, 4, N, N, 1], 3), ([1], 1), ([2, 1, 3], 3), ([5, 3, 6, 2, 4, N, N, 1], 6), (BST2, 4)],
      """
      class Solution:
          def kthSmallest(self, root, k):
              st = []; n = root
              while st or n:
                  while n:
                      st.append(n); n = n.left
                  n = st.pop(); k -= 1
                  if k == 0:
                      return n.val
                  n = n.right
      """, hint="In-order traversal visits BST values in ascending order."),
]

G13 = [
    F("Construct Binary Tree from Preorder and Inorder Traversal", 105, "Medium", """
        Given the preorder and inorder traversals of a binary tree with unique values, rebuild and return the tree.""" + TREE_NOTE + """

        Constraints:
        - 1 <= preorder.length == inorder.length <= 3000
        """, "buildTree(preorder:int[], inorder:int[])->TreeNode",
      [([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]), ([-1], [-1]), ([1, 2], [2, 1]), ([1, 2], [1, 2]), ([1, 2, 3, 4], [4, 3, 2, 1]), ([1, 2, 4, 5, 3, 6, 7], [4, 2, 5, 1, 6, 3, 7])],
      """
      class Solution:
          def buildTree(self, preorder, inorder):
              pos = {v: i for i, v in enumerate(inorder)}; it = iter(preorder)
              def build(l, r):
                  if l > r:
                      return None
                  v = next(it); n = TreeNode(v)
                  n.left = build(l, pos[v] - 1); n.right = build(pos[v] + 1, r)
                  return n
              return build(0, len(inorder) - 1)
      """, hint="The first preorder value is the root; find it in inorder to split left and right subtrees."),
    R("Serialize and Deserialize Binary Tree", 297, "Hard", """
        Design an algorithm to turn a binary tree into a string (`serialize`) and rebuild the same tree from that string (`deserialize`). The string format is up to you.

        The tests call `deserialize(serialize(root))` and check that the tree comes back unchanged.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 10^4
        """, "Codec", "serialize", "deserialize", "TreeNode",
      [[1, 2, 3, N, N, 4, 5], [], [1], [1, N, 2, N, 3], [5, 3, 8, 2, 4, 7, 9], [-1, 0, N, 1000, -1000]],
      """
      class Codec:
          def serialize(self, root):
              out = []
              def go(n):
                  if not n:
                      out.append('N'); return
                  out.append(str(n.val)); go(n.left); go(n.right)
              go(root)
              return ','.join(out)
          def deserialize(self, data):
              it = iter(data.split(','))
              def go():
                  v = next(it)
                  if v == 'N':
                      return None
                  n = TreeNode(int(v)); n.left = go(); n.right = go()
                  return n
              return go()
      """, hint="Preorder with explicit null markers is unambiguous."),
]

G14 = [
    D("Implement Trie (Prefix Tree)", 208, "Medium", """
        Implement a trie with these operations:

        - `insert(word)` inserts the string `word`.
        - `search(word)` returns `true` if `word` was inserted before.
        - `startsWith(prefix)` returns `true` if some inserted word starts with `prefix`.

        Words contain lowercase English letters.
        """, "Trie", "", ["insert(word:string)->void", "search(word:string)->bool", "startsWith(prefix:string)->bool"],
      [[("Trie", []), ("insert", ["apple"]), ("search", ["apple"]), ("search", ["app"]), ("startsWith", ["app"]), ("insert", ["app"]), ("search", ["app"])],
       [("Trie", []), ("search", ["a"]), ("startsWith", ["a"]), ("insert", ["a"]), ("search", ["a"]), ("startsWith", ["a"]), ("startsWith", ["ab"])],
       [("Trie", [])] + [("insert", ["w" + "abc"[i % 3] * (i % 7 + 1)]) for i in range(40)] + [("search", ["w" + "a" * k]) for k in range(1, 9)] + [("startsWith", ["wb" * k]) for k in (1, 2)]],
      """
      class Trie:
          def __init__(self):
              self.root = {}
          def insert(self, word):
              n = self.root
              for c in word:
                  n = n.setdefault(c, {})
              n['$'] = True
          def _find(self, s):
              n = self.root
              for c in s:
                  if c not in n:
                      return None
                  n = n[c]
              return n
          def search(self, word):
              n = self._find(word)
              return bool(n and '$' in n)
          def startsWith(self, prefix):
              return self._find(prefix) is not None
      """, hint="Each node stores its children by letter plus a flag for 'a word ends here'."),
    D("Design Add and Search Words Data Structure", 211, "Medium", """
        Design a data structure that supports adding words and searching with patterns.

        - `addWord(word)` adds a word.
        - `search(word)` returns `true` if any added word matches `word`. In a search pattern, `'.'` matches any single letter.

        Words contain lowercase English letters; patterns may also contain `'.'`.
        """, "WordDictionary", "", ["addWord(word:string)->void", "search(word:string)->bool"],
      [[("WordDictionary", []), ("addWord", ["bad"]), ("addWord", ["dad"]), ("addWord", ["mad"]), ("search", ["pad"]), ("search", ["bad"]), ("search", [".ad"]), ("search", ["b.."])],
       [("WordDictionary", []), ("addWord", ["a"]), ("addWord", ["ab"]), ("search", ["a"]), ("search", ["a."]), ("search", ["ab"]), ("search", [".a"]), ("search", [".."]), ("search", ["a.."])],
       [("WordDictionary", [])] + [("addWord", ["w%s" % ("xyz"[i % 3] * (i % 5 + 1))]) for i in range(30)] + [("search", [p]) for p in ("w.", "w..", "wx.", "w.....", "w", ".", "wz.z", "wyy")]],
      """
      class WordDictionary:
          def __init__(self):
              self.root = {}
          def addWord(self, word):
              n = self.root
              for c in word:
                  n = n.setdefault(c, {})
              n['$'] = True
          def search(self, word):
              def go(n, i):
                  if i == len(word):
                      return '$' in n
                  c = word[i]
                  if c == '.':
                      return any(go(ch, i + 1) for k, ch in n.items() if k != '$')
                  return c in n and go(n[c], i + 1)
              return go(self.root, 0)
      """, hint="Walk the trie normally; on '.', try every child with DFS."),
    F("Word Search II", 212, "Hard", """
        Given an `m x n` board of letters and a list of `words`, return all words that can be built from letters of sequentially adjacent cells (horizontally or vertically). The same cell may not be used twice in one word. The result may be in any order.

        Constraints:
        - 1 <= m, n <= 12
        - 1 <= words.length <= 3 * 10^4, each word 1 to 10 lowercase letters, all words unique
        """, "findWords(board:char[][], words:string[])->string[]",
      [([["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]], ["oath", "pea", "eat", "rain"]),
       ([["a", "b"], ["c", "d"]], ["abcb"]), ([["a"]], ["a"]), ([["a", "a"]], ["aaa"]),
       ([["a", "b", "c"], ["a", "e", "d"], ["a", "f", "g"]], ["abcdefg", "gfedcbaaa", "eaabcdgfa", "befa", "dgc", "ade"]),
       ([["a", "b"], ["c", "d"]], ["ab", "cb", "ad", "bd", "ac", "ca", "da", "bc", "db", "abcd", "acdb"])],
      """
      class Solution:
          def findWords(self, board, words):
              root = {}
              for w in words:
                  n = root
                  for c in w:
                      n = n.setdefault(c, {})
                  n['$'] = w
              R, C = len(board), len(board[0]); res = []
              def dfs(r, c, node):
                  ch = board[r][c]
                  nxt = node.get(ch)
                  if nxt is None:
                      return
                  if '$' in nxt:
                      res.append(nxt.pop('$'))
                  board[r][c] = '#'
                  for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                      rr, cc = r + dr, c + dc
                      if 0 <= rr < R and 0 <= cc < C and board[rr][cc] != '#':
                          dfs(rr, cc, nxt)
                  board[r][c] = ch
              for r in range(R):
                  for c in range(C):
                      dfs(r, c, root)
              return res
      """, cmp="sorted", hint="Build a trie of the words, then DFS from each cell following the trie."),
]

def ll(*arrs):
    return list(arrs)

G15 = [
    F("Top K Frequent Elements", 347, "Medium", """
        Given an integer array `nums` and an integer `k`, return the `k` most frequent elements in any order. The answer is guaranteed to be unique.

        Constraints:
        - 1 <= nums.length <= 10^5
        - 1 <= k <= number of distinct elements
        """, "topKFrequent(nums:int[], k:int)->int[]",
      [([1, 1, 1, 2, 2, 3], 2), ([1], 1), ([4, 4, 4, 5, 5, 6, 7, 7, 7, 7], 2), ([-1, -1], 1), ([1, 2], 2), ([3, 0, 1, 0], 1)],
      """
      class Solution:
          def topKFrequent(self, nums, k):
              return [x for x, _ in Counter(nums).most_common(k)]
      """, cmp="sorted", hint="Count with a hash map, then use a heap or bucket sort by frequency."),
    F("Merge k Sorted Lists", 23, "Hard", """
        You are given an array of `k` sorted linked lists. Merge them all into one sorted linked list and return its head.

        Constraints:
        - 0 <= k <= 10^4
        - total number of nodes <= 10^4
        """, "mergeKLists(lists:ListNode[])->ListNode",
      [([[1, 4, 5], [1, 3, 4], [2, 6]],), ([],), ([[]],), ([[1], [0]],), ([[], [1], []],), ([[5, 6, 7], [1, 2], [3]],)],
      """
      class Solution:
          def mergeKLists(self, lists):
              h = []
              for i, n in enumerate(lists):
                  if n:
                      heappush(h, (n.val, i, n))
              d = t = ListNode()
              while h:
                  _, i, n = heappop(h)
                  t.next = n; t = n
                  if n.next:
                      heappush(h, (n.next.val, i, n.next))
              return d.next
      """, hint="A min-heap holding the current head of each list always yields the next smallest node."),
    D("Kth Largest Element in a Stream", 703, "Easy", """
        Design a class that tracks the `k`-th largest element of a growing stream (the k-th largest in sorted order, counting duplicates).

        - `KthLargest(k, nums)` initializes with the integer `k` and the starting numbers.
        - `add(val)` appends `val` to the stream and returns the current k-th largest element.

        `add` is only called when the stream has at least `k` numbers.
        """, "KthLargest", "k:int, nums:int[]", ["add(val:int)->int"],
      [[("KthLargest", [3, [4, 5, 8, 2]]), ("add", [3]), ("add", [5]), ("add", [10]), ("add", [9]), ("add", [4])],
       [("KthLargest", [1, []]), ("add", [-3]), ("add", [-2]), ("add", [-4]), ("add", [0]), ("add", [4])],
       [("KthLargest", [2, [0]]), ("add", [-1]), ("add", [1]), ("add", [-2]), ("add", [-4]), ("add", [3])]],
      """
      class KthLargest:
          def __init__(self, k, nums):
              self.k = k; self.h = list(nums); heapify(self.h)
              while len(self.h) > k:
                  heappop(self.h)
          def add(self, val):
              heappush(self.h, val)
              if len(self.h) > self.k:
                  heappop(self.h)
              return self.h[0]
      """, hint="Keep a min-heap of the k largest values; its root is the answer."),
    F("Kth Largest Element in an Array", 215, "Medium", """
        Return the `k`-th largest element of `nums` in sorted order (not the k-th distinct element).

        Constraints:
        - 1 <= k <= nums.length <= 10^5
        """, "findKthLargest(nums:int[], k:int)->int",
      [([3, 2, 1, 5, 6, 4], 2), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), ([1], 1), ([2, 1], 2), ([-1, -1], 2), ([7, 6, 5, 4, 3, 2, 1], 5)],
      """
      class Solution:
          def findKthLargest(self, nums, k):
              return nlargest(k, nums)[-1]
      """, hint="A size-k min-heap, or quickselect for O(n) average."),
    F("Last Stone Weight", 1046, "Easy", """
        Each turn, take the two heaviest stones with weights `x <= y`. If `x == y` both are destroyed; otherwise the stone `x` is destroyed and `y` becomes `y - x`. Return the weight of the last remaining stone, or 0 if none remain.

        Constraints:
        - 1 <= stones.length <= 30
        - 1 <= stones[i] <= 1000
        """, "lastStoneWeight(stones:int[])->int",
      [([2, 7, 4, 1, 8, 1],), ([1],), ([2, 2],), ([10, 4, 2, 10],), ([3, 3, 3],), ([1, 1, 2, 3, 5, 8],)],
      """
      class Solution:
          def lastStoneWeight(self, stones):
              h = [-s for s in stones]; heapify(h)
              while len(h) > 1:
                  a = -heappop(h); b = -heappop(h)
                  if a != b:
                      heappush(h, -(a - b))
              return -h[0] if h else 0
      """, hint="A max-heap gives the two heaviest stones each turn."),
    F("K Closest Points to Origin", 973, "Medium", """
        Given `points[i] = [x, y]` and an integer `k`, return the `k` points closest to the origin (0, 0) by Euclidean distance. The answer may be in any order and is guaranteed to be unique apart from ordering.

        Constraints:
        - 1 <= k <= points.length <= 10^4
        """, "kClosest(points:int[][], k:int)->int[][]",
      [([[1, 3], [-2, 2]], 1), ([[3, 3], [5, -1], [-2, 4]], 2), ([[0, 1], [1, 0]], 2), ([[1, 1]], 1), ([[2, 2], [2, 2], [1, 1]], 1), ([[5, 5], [1, 1], [3, 3], [2, 2]], 3)],
      """
      class Solution:
          def kClosest(self, points, k):
              return nsmallest(k, points, key=lambda p: p[0] * p[0] + p[1] * p[1])
      """, cmp="sorted", hint="Compare squared distances; a size-k max-heap or a full sort both work."),
    F("Task Scheduler", 621, "Medium", """
        `tasks` lists CPU tasks as capital letters. Each task takes one unit of time, and the same letter must be separated by at least `n` units of cooldown (idle or other tasks). Return the minimum number of time units needed to finish all tasks.

        Constraints:
        - 1 <= tasks.length <= 10^4
        - 0 <= n <= 100
        """, "leastInterval(tasks:string[], n:int)->int",
      [(["A", "A", "A", "B", "B", "B"], 2), (["A", "C", "A", "B", "D", "B"], 1), (["A", "A", "A", "B", "B", "B"], 3), (["A"], 5), (["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2), (["A", "B", "C"], 0)],
      """
      class Solution:
          def leastInterval(self, tasks, n):
              cnt = Counter(tasks); mx = max(cnt.values()); nmax = sum(1 for v in cnt.values() if v == mx)
              return max(len(tasks), (mx - 1) * (n + 1) + nmax)
      """, hint="The most frequent task determines the frame size; other tasks fill the idle slots."),
    D("Find Median from Data Stream", 295, "Hard", """
        Design a structure for a growing stream of integers that can report the median at any time.

        - `addNum(num)` adds an integer.
        - `findMedian()` returns the median of all numbers so far: the middle value, or the mean of the two middle values when the count is even.

        `findMedian` is only called after at least one number was added.
        """, "MedianFinder", "", ["addNum(num:int)->void", "findMedian()->double"],
      [[("MedianFinder", []), ("addNum", [1]), ("addNum", [2]), ("findMedian", []), ("addNum", [3]), ("findMedian", [])],
       [("MedianFinder", []), ("addNum", [-1]), ("findMedian", []), ("addNum", [-2]), ("findMedian", []), ("addNum", [-3]), ("findMedian", []), ("addNum", [-4]), ("findMedian", []), ("addNum", [-5]), ("findMedian", [])],
       [("MedianFinder", [])] + [x for i in range(150) for x in (("addNum", [(i * 7919) % 1000 - 500]), ("findMedian", []))]],
      """
      class MedianFinder:
          def __init__(self):
              self.lo = []; self.hi = []
          def addNum(self, num):
              heappush(self.lo, -num); heappush(self.hi, -heappop(self.lo))
              if len(self.hi) > len(self.lo):
                  heappush(self.lo, -heappop(self.hi))
          def findMedian(self):
              if len(self.lo) > len(self.hi):
                  return float(-self.lo[0])
              return (-self.lo[0] + self.hi[0]) / 2
      """, hint="Two heaps: a max-heap for the lower half and a min-heap for the upper half, kept balanced."),
]
