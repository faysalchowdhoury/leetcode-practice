from dsl import F, D, R

# LeetCode-only problems, part 2: trees, heaps, backtracking, graphs, DP, intervals, matrix, math, bits.
N = None
TREE_NOTE = "\n\nIn the tests a binary tree is shown in level order, with `null` for a missing child (for example `[3,9,20,null,null,15,7]`)."
BIG = [3, 5, 1, 6, 2, 0, 8, N, N, 7, 4]

L_TREE_DFS = [
    F("Symmetric Tree", 101, "Easy", """
        Return `true` if a binary tree is a mirror image of itself (symmetric around its centre).""" + TREE_NOTE + """

        Constraints:
        - 1 <= number of nodes <= 1000
        """, "isSymmetric(root:TreeNode)->bool",
      [([1, 2, 2, 3, 4, 4, 3],), ([1, 2, 2, N, 3, N, 3],), ([1],), ([1, 2, 2, 2, N, 2],), ([1, 2, 2, N, 3, 3],), ([1, 2],)],
      """
      class Solution:
          def isSymmetric(self, root):
              def mirror(a, b):
                  if not a and not b:
                      return True
                  if not a or not b or a.val != b.val:
                      return False
                  return mirror(a.left, b.right) and mirror(a.right, b.left)
              return mirror(root.left, root.right) if root else True
      """, hint="Compare the left subtree with the mirrored right subtree."),
    F("Path Sum", 112, "Easy", """
        Return `true` if the tree has a root-to-leaf path whose node values add up to `targetSum`.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 5000
        """, "hasPathSum(root:TreeNode, targetSum:int)->bool",
      [([5, 4, 8, 11, N, 13, 4, 7, 2, N, N, N, 1], 22), ([1, 2, 3], 5), ([], 0), ([1, 2], 1), ([1], 1), ([1, -2, -3, 1, 3, -2, N, -1], -1)],
      """
      class Solution:
          def hasPathSum(self, root, targetSum):
              if not root:
                  return False
              if not root.left and not root.right:
                  return root.val == targetSum
              return self.hasPathSum(root.left, targetSum - root.val) or self.hasPathSum(root.right, targetSum - root.val)
      """, hint="Subtract the node value as you go down; check at the leaves."),
    F("Sum Root to Leaf Numbers", 129, "Medium", """
        Each root-to-leaf path of a tree with digits 0-9 forms a number (for example 1 -> 2 -> 3 is 123). Return the sum of all those numbers.""" + TREE_NOTE + """

        Constraints:
        - 1 <= number of nodes <= 1000, depth <= 10
        """, "sumNumbers(root:TreeNode)->int",
      [([1, 2, 3],), ([4, 9, 0, 5, 1],), ([0],), ([1, 0],), ([9, 8, 7, 6, 5],), ([1, 2, 3, 4, 5, 6, 7],)],
      """
      class Solution:
          def sumNumbers(self, root):
              def go(n, cur):
                  if not n:
                      return 0
                  cur = cur * 10 + n.val
                  if not n.left and not n.right:
                      return cur
                  return go(n.left, cur) + go(n.right, cur)
              return go(root, 0)
      """, hint="Carry the number built so far down the recursion."),
    F("Flatten Binary Tree to Linked List", 114, "Medium", """
        Flatten the tree **in place** into a "linked list" that uses the `right` pointers: the nodes must appear in pre-order, every `left` pointer must be null.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 2000
        """, "flatten(root:TreeNode)->void",
      [([1, 2, 5, 3, 4, N, 6],), ([],), ([0],), ([1, 2],), ([1, N, 2],), ([1, 2, 3, 4],)],
      """
      class Solution:
          def flatten(self, root):
              cur = root
              while cur:
                  if cur.left:
                      p = cur.left
                      while p.right:
                          p = p.right
                      p.right = cur.right; cur.right = cur.left; cur.left = None
                  cur = cur.right
      """, inplace="root", hint="For each node, attach its right subtree to the rightmost node of its left subtree, then move the left subtree to the right."),
    F("Count Complete Tree Nodes", 222, "Easy", """
        Return the number of nodes in a **complete** binary tree (every level is full except possibly the last, which is filled from the left). Aim for better than O(n).""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 5 * 10^4
        """, "countNodes(root:TreeNode)->int",
      [([1, 2, 3, 4, 5, 6],), ([],), ([1],), ([1, 2, 3, 4],), ([1, 2, 3, 4, 5, 6, 7],), ([1, 2, 3, 4, 5],)],
      """
      class Solution:
          def countNodes(self, root):
              if not root:
                  return 0
              l = r = root; hl = hr = 0
              while l: l = l.left; hl += 1
              while r: r = r.right; hr += 1
              if hl == hr:
                  return 2 ** hl - 1
              return 1 + self.countNodes(root.left) + self.countNodes(root.right)
      """, hint="If the leftmost and rightmost depths match the subtree is perfect and its size is 2^h - 1."),
    F("Lowest Common Ancestor of a Binary Tree", 236, "Medium", """
        Given a binary tree and two node values `p` and `q` that both exist in it, return the **value** of their lowest common ancestor (the deepest node having both as descendants; a node is its own descendant).""" + TREE_NOTE + """

        Constraints:
        - 2 <= number of nodes <= 10^5, all values unique, p != q
        """, "lowestCommonAncestor(root:TreeNode, p:int, q:int)->int",
      [(BIG, 5, 1), (BIG, 5, 4), ([1, 2], 1, 2), (BIG, 6, 4), (BIG, 7, 8), (BIG, 0, 8)],
      """
      class Solution:
          def lowestCommonAncestor(self, root, p, q):
              def go(n):
                  if not n or n.val in (p, q):
                      return n
                  l, r = go(n.left), go(n.right)
                  return n if l and r else (l or r)
              return go(root).val
      """, hint="If p and q are found in different subtrees, the current node is the answer."),
]

L_TREE_BFS = [
    F("Binary Tree Zigzag Level Order Traversal", 103, "Medium", """
        Return the zigzag level order traversal: left to right on the first level, right to left on the second, and so on.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 2000
        """, "zigzagLevelOrder(root:TreeNode)->int[][]",
      [([3, 9, 20, N, N, 15, 7],), ([1],), ([],), ([1, 2, 3, 4, N, N, 5],), ([1, 2, 3, 4, 5, 6, 7],)],
      """
      class Solution:
          def zigzagLevelOrder(self, root):
              if not root:
                  return []
              res = []; q = deque([root]); flip = False
              while q:
                  vals = [n.val for n in q]
                  res.append(vals[::-1] if flip else vals); flip = not flip
                  for _ in range(len(q)):
                      n = q.popleft()
                      if n.left: q.append(n.left)
                      if n.right: q.append(n.right)
              return res
      """, hint="Level order, reversing every other level."),
    F("Average of Levels in Binary Tree", 637, "Easy", """
        Return the average value of the nodes on each level of the tree, as an array.""" + TREE_NOTE + """

        Constraints:
        - 1 <= number of nodes <= 10^4
        - answers within 10^-5 of the true value are accepted
        """, "averageOfLevels(root:TreeNode)->double[]",
      [([3, 9, 20, N, N, 15, 7],), ([3, 9, 20, 15, 7],), ([1],), ([2147483647, 2147483647, 2147483647],), ([1, 2, 3, 4, 5],)],
      """
      class Solution:
          def averageOfLevels(self, root):
              res = []; q = deque([root])
              while q:
                  vals = [n.val for n in q]; res.append(sum(vals) / len(vals))
                  for _ in range(len(q)):
                      n = q.popleft()
                      if n.left: q.append(n.left)
                      if n.right: q.append(n.right)
              return res
      """, cmp="float_arr", hint="BFS by level; sum and count each level."),
    F("Populating Next Right Pointers in Each Node II", 117, "Medium", """
        Every node has an extra `next` pointer. Fill each `next` pointer so it points to the node immediately to its right on the same level, or null if it is the last node of its level. The tree is any binary tree (not necessarily perfect).

        The checker walks the finished tree and reports the values of each level, verifying every `next` pointer along the way.""" + TREE_NOTE + """

        Constraints:
        - 0 <= number of nodes <= 6000
        """, "connect(root:NextTree)->NextTree",
      [([1, 2, 3, 4, 5, N, 7],), ([],), ([1],), ([1, 2, 3, 4, N, N, 5],), ([2, 1, 3, 0, 7, 9, 1, 2, N, 1, 0, N, N, 8, 8, N, N, N, N, 7],), ([1, N, 2, 3],)],
      """
      class Solution:
          def connect(self, root):
              level = [root] if root else []
              while level:
                  for a, b in zip(level, level[1:]):
                      a.next = b
                  level = [c for n in level for c in (n.left, n.right) if c]
              return root
      """, hint="Process level by level, linking neighbours; or reuse the `next` links you already made to walk the level."),
]

L_BST = [
    F("Minimum Absolute Difference in BST", 530, "Easy", """
        Return the minimum absolute difference between the values of any two different nodes of a BST.""" + TREE_NOTE + """

        Constraints:
        - 2 <= number of nodes <= 10^4
        """, "getMinimumDifference(root:TreeNode)->int",
      [([4, 2, 6, 1, 3],), ([1, 0, 48, N, N, 12, 49],), ([1, N, 3, 2],), ([5, 3, 8],), ([236, 104, 701, N, 227, N, 911],), ([10, 5, 15, 2, 7, 12, 20],)],
      """
      class Solution:
          def getMinimumDifference(self, root):
              vals = []
              def go(n):
                  if n:
                      go(n.left); vals.append(n.val); go(n.right)
              go(root)
              return min(b - a for a, b in zip(vals, vals[1:]))
      """, hint="An in-order traversal gives sorted values; compare neighbours."),
    D("Binary Search Tree Iterator", 173, "Medium", """
        Implement an iterator over the in-order traversal of a BST.

        - `BSTIterator(root)` initializes the iterator with the root of the tree.
        - `next()` returns the next smallest number.
        - `hasNext()` returns `true` if a next number exists.

        `next` is only called when `hasNext` is true. Aim for O(h) memory.""" + TREE_NOTE, "BSTIterator", "root:TreeNode", ["next()->int", "hasNext()->bool"],
      [[("BSTIterator", [[7, 3, 15, N, N, 9, 20]]), ("next", []), ("next", []), ("hasNext", []), ("next", []), ("hasNext", []), ("next", []), ("hasNext", [])],
       [("BSTIterator", [[1]]), ("hasNext", []), ("next", []), ("hasNext", [])],
       [("BSTIterator", [[8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]])] + [x for _ in range(15) for x in (("hasNext", []), ("next", []))] + [("hasNext", [])]],
      """
      class BSTIterator:
          def __init__(self, root):
              self.st = []; self._push(root)
          def _push(self, n):
              while n:
                  self.st.append(n); n = n.left
          def next(self):
              n = self.st.pop(); self._push(n.right); return n.val
          def hasNext(self):
              return bool(self.st)
      """, hint="Keep a stack holding the path to the next node (controlled in-order traversal)."),
]

L_BUILD = [
    F("Construct Binary Tree from Inorder and Postorder Traversal", 106, "Medium", """
        Given the inorder and postorder traversals of a binary tree with unique values, rebuild and return the tree.""" + TREE_NOTE + """

        Constraints:
        - 1 <= inorder.length == postorder.length <= 3000
        """, "buildTree(inorder:int[], postorder:int[])->TreeNode",
      [([9, 3, 15, 20, 7], [9, 15, 7, 20, 3]), ([-1], [-1]), ([2, 1], [2, 1]), ([1, 2], [2, 1]), ([4, 2, 5, 1, 6, 3, 7], [4, 5, 2, 6, 7, 3, 1])],
      """
      class Solution:
          def buildTree(self, inorder, postorder):
              pos = {v: i for i, v in enumerate(inorder)}; post = postorder[:]
              def build(l, r):
                  if l > r:
                      return None
                  v = post.pop(); n = TreeNode(v)
                  n.right = build(pos[v] + 1, r); n.left = build(l, pos[v] - 1)
                  return n
              return build(0, len(inorder) - 1)
      """, hint="The last postorder value is the root; build the right subtree first when consuming from the end."),
    F("Convert Sorted Array to Binary Search Tree", 108, "Easy", """
        Convert a sorted (ascending) array into a **height-balanced** binary search tree. Any valid balanced BST is accepted.""" + TREE_NOTE + """

        Constraints:
        - 1 <= nums.length <= 10^4, strictly increasing
        """, "sortedArrayToBST(nums:int[])->TreeNode",
      [([-10, -3, 0, 5, 9],), ([1, 3],), ([1],), ([1, 2, 3, 4, 5, 6, 7],), ([0, 1, 2, 3, 4, 5],)],
      """
      class Solution:
          def sortedArrayToBST(self, nums):
              def build(l, r):
                  if l > r:
                      return None
                  m = (l + r) // 2
                  return TreeNode(nums[m], build(l, m - 1), build(m + 1, r))
              return build(0, len(nums) - 1)
      """, cmp="bst_bal", hint="Pick the middle element as root and recurse on each half."),
    F("Construct Quad Tree", 427, "Medium", """
        Given an `n x n` grid of 0s and 1s (n is a power of 2), build its quad tree. A node is a leaf if its whole region has the same value; otherwise split the region into four equal quadrants (`topLeft`, `topRight`, `bottomLeft`, `bottomRight`).

        Each node has `isLeaf` and `val` (the value of a leaf; arbitrary for non-leaf nodes). The checker shows the tree in level order as `[isLeaf, val]` pairs (with `val` reported as 1 for non-leaf nodes), listing the four children of every non-leaf node and `null` for absent entries.

        Constraints:
        - n == grid.length == grid[i].length, n == 2^x with 0 <= x <= 6
        """, "construct(grid:int[][])->QuadTree",
      [([[0, 1], [1, 0]],), ([[1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0]],), ([[1]],), ([[0, 0], [0, 0]],), ([[1, 1], [1, 0]],)],
      """
      class Solution:
          def construct(self, grid):
              def build(r, c, n):
                  if n == 1:
                      return Node(grid[r][c] == 1, True)
                  h = n // 2
                  tl, tr, bl, br = build(r, c, h), build(r, c + h, h), build(r + h, c, h), build(r + h, c + h, h)
                  if all(x.isLeaf for x in (tl, tr, bl, br)) and len({x.val for x in (tl, tr, bl, br)}) == 1:
                      return Node(tl.val, True)
                  return Node(True, False, tl, tr, bl, br)
              return build(0, 0, len(grid))
      """, hint="Recurse on the four quadrants; if all four are leaves with the same value, merge them into one leaf."),
]

L_MERGE = [
    F("Sort List", 148, "Medium", """
        Sort a linked list in ascending order. Aim for O(n log n) time.

        Constraints:
        - 0 <= n <= 5 * 10^4
        """, "sortList(head:ListNode)->ListNode",
      [([4, 2, 1, 3],), ([-1, 5, 3, 4, 0],), ([],), ([1],), ([3, 3, 1, 1, 2],), ([5, 4, 3, 2, 1, 0],)],
      """
      class Solution:
          def sortList(self, head):
              if not head or not head.next:
                  return head
              slow, fast = head, head.next
              while fast and fast.next:
                  slow = slow.next; fast = fast.next.next
              mid = slow.next; slow.next = None
              a, b = self.sortList(head), self.sortList(mid)
              d = t = ListNode()
              while a and b:
                  if a.val <= b.val:
                      t.next = a; a = a.next
                  else:
                      t.next = b; b = b.next
                  t = t.next
              t.next = a or b
              return d.next
      """, hint="Merge sort: split at the middle, sort both halves, merge."),
]

L_HEAP = [
    F("IPO", 502, "Hard", """
        You can complete at most `k` distinct projects. Project `i` needs at least `capital[i]` capital to start and adds `profits[i]` to your capital when finished. You start with capital `w`. Return the maximum capital you can end with.

        Constraints:
        - 1 <= k <= 10^5, 0 <= w <= 10^9, n == profits.length == capital.length <= 10^5
        """, "findMaximizedCapital(k:int, w:int, profits:int[], capital:int[])->int",
      [(2, 0, [1, 2, 3], [0, 1, 1]), (3, 0, [1, 2, 3], [0, 1, 2]), (1, 0, [1, 2, 3], [1, 1, 2]), (2, 1, [5, 3, 9], [2, 0, 10]), (0, 5, [1], [0]), (10, 0, [1, 2, 3], [0, 1, 2])],
      """
      class Solution:
          def findMaximizedCapital(self, k, w, profits, capital):
              projects = sorted(zip(capital, profits)); h = []; i = 0
              for _ in range(k):
                  while i < len(projects) and projects[i][0] <= w:
                      heappush(h, -projects[i][1]); i += 1
                  if not h:
                      break
                  w -= heappop(h)
              return w
      """, hint="Among the projects you can afford, always take the most profitable one (max-heap)."),
    F("Find K Pairs with Smallest Sums", 373, "Medium", """
        Given two sorted arrays `nums1` and `nums2`, return the `k` pairs `(u, v)` (one element from each array) with the smallest sums `u + v`. If several answers exist, any is accepted as long as the multiset of sums is the same.

        Constraints:
        - 1 <= nums1.length, nums2.length <= 10^5, 1 <= k <= 10^4
        """, "kSmallestPairs(nums1:int[], nums2:int[], k:int)->int[][]",
      [([1, 7, 11], [2, 4, 6], 3), ([1, 1, 2], [1, 2, 3], 2), ([1, 2], [3], 3), ([1, 2, 4, 5, 6], [3, 5, 7, 9], 3), ([1], [1], 1), ([0, 0, 0, 0, 0], [-3, 22, 35, 56, 76], 22)],
      """
      class Solution:
          def kSmallestPairs(self, nums1, nums2, k):
              if not nums1 or not nums2:
                  return []
              h = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]; heapify(h); res = []
              while h and len(res) < k:
                  s, i, j = heappop(h); res.append([nums1[i], nums2[j]])
                  if j + 1 < len(nums2):
                      heappush(h, (nums1[i] + nums2[j + 1], i, j + 1))
              return res
      """, cmp="kpairs", hint="Heap of candidates: pop the smallest pair and push its right neighbour in nums2."),
]

L_BACK = [
    F("N-Queens II", 52, "Hard", """
        Return the number of distinct ways to place `n` queens on an `n x n` board so that no two attack each other.

        Constraints:
        - 1 <= n <= 9
        """, "totalNQueens(n:int)->int",
      [(4,), (1,), (5,), (6,), (8,), (2,)],
      """
      class Solution:
          def totalNQueens(self, n):
              cols = set(); d1 = set(); d2 = set()
              def go(r):
                  if r == n:
                      return 1
                  t = 0
                  for c in range(n):
                      if c in cols or r - c in d1 or r + c in d2:
                          continue
                      cols.add(c); d1.add(r - c); d2.add(r + c)
                      t += go(r + 1)
                      cols.remove(c); d1.remove(r - c); d2.remove(r + c)
                  return t
              return go(0)
      """, hint="Same search as N-Queens, but only count."),
    F("Combinations", 77, "Medium", """
        Return all combinations of `k` numbers chosen from `1..n`, in any order.

        Constraints:
        - 1 <= n <= 20, 1 <= k <= n
        """, "combine(n:int, k:int)->int[][]",
      [(4, 2), (1, 1), (5, 3), (3, 3), (6, 1), (6, 4)],
      """
      class Solution:
          def combine(self, n, k):
              return [list(c) for c in combinations(range(1, n + 1), k)]
      """, cmp="sorted_deep", hint="Choose the next number from the ones larger than the last chosen."),
]

L_GRAPH = [
    F("Evaluate Division", 399, "Medium", """
        `equations[i] = [A, B]` with `values[i]` means `A / B = values[i]`. For each query `[C, D]` return `C / D`, or `-1.0` if it cannot be determined (including when a variable never appears).

        Constraints:
        - 1 <= equations.length <= 20, 0.0 < values[i] <= 20.0
        - answers within 10^-5 are accepted
        """, "calcEquation(equations:string[][], values:double[], queries:string[][])->double[]",
      [([["a", "b"], ["b", "c"]], [2.0, 3.0], [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]), ([["a", "b"], ["b", "c"], ["bc", "cd"]], [1.5, 2.5, 5.0], [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]]), ([["a", "b"]], [0.5], [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]]), ([["x1", "x2"], ["x2", "x3"], ["x3", "x4"], ["x4", "x5"]], [3.0, 4.0, 5.0, 6.0], [["x1", "x5"], ["x5", "x2"], ["x2", "x4"], ["x2", "x2"], ["x2", "x9"], ["x9", "x9"]])],
      """
      class Solution:
          def calcEquation(self, equations, values, queries):
              g = defaultdict(dict)
              for (a, b), v in zip(equations, values):
                  g[a][b] = v; g[b][a] = 1 / v
              def solve(s, t):
                  if s not in g or t not in g:
                      return -1.0
                  seen = {s}; q = deque([(s, 1.0)])
                  while q:
                      x, acc = q.popleft()
                      if x == t:
                          return acc
                      for y, w in g[x].items():
                          if y not in seen:
                              seen.add(y); q.append((y, acc * w))
                  return -1.0
              return [solve(a, b) for a, b in queries]
      """, cmp="float_arr", hint="Build a weighted graph (A -> B with weight A/B, and the reverse) and multiply weights along a path."),
    F("Snakes and Ladders", 909, "Medium", """
        An `n x n` board is numbered `1..n^2` in a boustrophedon (zig-zag) pattern, starting at the bottom-left and alternating direction each row. `board[r][c]` is `-1`, or the destination of a snake/ladder on that square. Starting on square 1, each move rolls a die: go to any square `curr + 1 .. curr + 6`; if that square has a snake or ladder you must take it (only once per move). Return the fewest moves to reach square `n^2`, or -1.

        Constraints:
        - 2 <= n <= 20
        """, "snakesAndLadders(board:int[][])->int",
      [([[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, 35, -1, -1, 13, -1], [-1, -1, -1, -1, -1, -1], [-1, 15, -1, -1, -1, -1]],), ([[-1, -1], [-1, 3]],), ([[1, 1, -1], [1, 1, 1], [-1, 1, 1]],), ([[-1, -1, -1], [-1, 9, 8], [-1, 8, 9]],), ([[-1, 1, 2, -1], [2, 13, 15, -1], [-1, 10, -1, -1], [-1, 6, 2, 8]],)],
      """
      class Solution:
          def snakesAndLadders(self, board):
              n = len(board)
              def cell(s):
                  r, c = divmod(s - 1, n)
                  row = n - 1 - r
                  col = c if r % 2 == 0 else n - 1 - c
                  return board[row][col]
              seen = {1}; q = deque([(1, 0)])
              while q:
                  s, d = q.popleft()
                  if s == n * n:
                      return d
                  for t in range(s + 1, min(s + 6, n * n) + 1):
                      dest = cell(t)
                      if dest != -1:
                          t = dest
                      if t not in seen:
                          seen.add(t); q.append((t, d + 1))
              return -1
      """, hint="BFS over square numbers; convert a square number to a row/column carefully."),
    F("Minimum Genetic Mutation", 433, "Medium", """
        A gene is an 8-character string over `A, C, G, T`. One mutation changes a single character. Given `startGene`, `endGene` and a `bank` of valid genes, return the minimum number of mutations to turn `startGene` into `endGene` where every intermediate gene must be in the bank, or -1 if impossible. The start gene need not be in the bank.

        Constraints:
        - 0 <= bank.length <= 10
        """, "minMutation(startGene:string, endGene:string, bank:string[])->int",
      [("AACCGGTT", "AACCGGTA", ["AACCGGTA"]), ("AACCGGTT", "AAACGGTA", ["AACCGGTA", "AACCGCTA", "AAACGGTA"]), ("AAAAACCC", "AACCCCCC", ["AAAACCCC", "AAACCCCC", "AACCCCCC"]), ("AACCGGTT", "AACCGGTA", []), ("AAAAAAAA", "AAAAAAAA", []), ("AACCGGTT", "GGCCGGTT", ["AACCGGTA"])],
      """
      class Solution:
          def minMutation(self, startGene, endGene, bank):
              bank = set(bank); q = deque([(startGene, 0)]); seen = {startGene}
              while q:
                  g, d = q.popleft()
                  if g == endGene:
                      return d
                  for i in range(len(g)):
                      for ch in 'ACGT':
                          x = g[:i] + ch + g[i + 1:]
                          if x in bank and x not in seen:
                              seen.add(x); q.append((x, d + 1))
              return -1
      """, hint="BFS exactly like Word Ladder."),
]

L_DP = [
    F("Triangle", 120, "Medium", """
        Given a `triangle` array, return the minimum path sum from top to bottom. At each step you may move to an adjacent number in the row below (index `i` or `i + 1`).

        Constraints:
        - 1 <= triangle.length <= 200
        """, "minimumTotal(triangle:int[][])->int",
      [([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]],), ([[-10]],), ([[1], [2, 3]],), ([[-1], [2, 3], [1, -1, -3]],), ([[5], [7, 2], [1, 3, 4], [8, 9, 6, 10]],)],
      """
      class Solution:
          def minimumTotal(self, triangle):
              dp = triangle[-1][:]
              for row in range(len(triangle) - 2, -1, -1):
                  for i in range(row + 1):
                      dp[i] = triangle[row][i] + min(dp[i], dp[i + 1])
              return dp[0]
      """, hint="Work bottom-up, so each cell takes the cheaper of the two cells below it."),
    F("Minimum Path Sum", 64, "Medium", """
        Given an `m x n` grid of non-negative numbers, find a path from the top-left to the bottom-right (moving only right or down) that minimises the sum of the numbers along it, and return that sum.

        Constraints:
        - 1 <= m, n <= 200
        """, "minPathSum(grid:int[][])->int",
      [([[1, 3, 1], [1, 5, 1], [4, 2, 1]],), ([[1, 2, 3], [4, 5, 6]],), ([[5]],), ([[1, 2], [1, 1]],), ([[1, 2, 5], [3, 2, 1]],)],
      """
      class Solution:
          def minPathSum(self, grid):
              R, C = len(grid), len(grid[0]); dp = [float('inf')] * C; dp[0] = 0
              for r in range(R):
                  for c in range(C):
                      best = dp[c] if r else float('inf')
                      if c: best = min(best, dp[c - 1])
                      dp[c] = grid[r][c] + (best if (r or c) else 0)
              return dp[-1]
      """, hint="cost(r, c) = grid[r][c] + min(cost(r-1, c), cost(r, c-1))."),
    F("Unique Paths II", 63, "Medium", """
        Like Unique Paths, but some cells are obstacles (`1`) that cannot be entered (`0` is free). Return the number of paths from the top-left to the bottom-right moving only right or down.

        Constraints:
        - 1 <= m, n <= 100
        """, "uniquePathsWithObstacles(obstacleGrid:int[][])->int",
      [([[0, 0, 0], [0, 1, 0], [0, 0, 0]],), ([[0, 1], [0, 0]],), ([[1]],), ([[0]],), ([[0, 0], [1, 1], [0, 0]],), ([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],)],
      """
      class Solution:
          def uniquePathsWithObstacles(self, obstacleGrid):
              C = len(obstacleGrid[0]); dp = [0] * C; dp[0] = 1
              for row in obstacleGrid:
                  for c in range(C):
                      if row[c]:
                          dp[c] = 0
                      elif c:
                          dp[c] += dp[c - 1]
              return dp[-1]
      """, hint="Same DP as Unique Paths, but an obstacle cell has zero paths."),
    F("Best Time to Buy and Sell Stock III", 123, "Hard", """
        `prices[i]` is the price on day `i`. You may complete **at most two** transactions (and hold at most one share at a time). Return the maximum profit.

        Constraints:
        - 1 <= prices.length <= 10^5
        """, "maxProfit(prices:int[])->int",
      [([3, 3, 5, 0, 0, 3, 1, 4],), ([1, 2, 3, 4, 5],), ([7, 6, 4, 3, 1],), ([1],), ([1, 2, 4, 2, 5, 7, 2, 4, 9, 0],), ([2, 1, 2, 0, 1],)],
      """
      class Solution:
          def maxProfit(self, prices):
              b1 = b2 = -float('inf'); s1 = s2 = 0
              for p in prices:
                  b1 = max(b1, -p); s1 = max(s1, b1 + p); b2 = max(b2, s1 - p); s2 = max(s2, b2 + p)
              return s2
      """, hint="Four states: after first buy, first sell, second buy, second sell."),
    F("Best Time to Buy and Sell Stock IV", 188, "Hard", """
        Same as before, but you may complete **at most `k`** transactions. Return the maximum profit.

        Constraints:
        - 1 <= prices.length <= 1000, 0 <= k <= 100
        """, "maxProfit(k:int, prices:int[])->int",
      [(2, [2, 4, 1]), (2, [3, 2, 6, 5, 0, 3]), (1, [1, 2]), (3, [1, 2, 4, 2, 5, 7, 2, 4, 9, 0]), (0, [1, 2]), (100, [1, 2, 3, 4, 5])],
      """
      class Solution:
          def maxProfit(self, k, prices):
              if k >= len(prices) // 2:
                  return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))
              buy = [-float('inf')] * (k + 1); sell = [0] * (k + 1)
              for p in prices:
                  for j in range(1, k + 1):
                      buy[j] = max(buy[j], sell[j - 1] - p); sell[j] = max(sell[j], buy[j] + p)
              return sell[k]
      """, hint="dp[j] for each transaction count j; if k is large it degenerates into Stock II."),
    F("Maximal Square", 221, "Medium", """
        In a binary matrix of `'0'` and `'1'`, find the largest square containing only `'1'` and return its **area**.

        Constraints:
        - 1 <= m, n <= 300
        """, "maximalSquare(matrix:char[][])->int",
      [([["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]],), ([["0", "1"], ["1", "0"]],), ([["0"]],), ([["1"]],), ([["1", "1"], ["1", "1"]],), ([["1", "1", "1"], ["1", "1", "1"], ["0", "1", "1"]],)],
      """
      class Solution:
          def maximalSquare(self, matrix):
              R, C = len(matrix), len(matrix[0]); dp = [[0] * (C + 1) for _ in range(R + 1)]; best = 0
              for r in range(R):
                  for c in range(C):
                      if matrix[r][c] == '1':
                          dp[r + 1][c + 1] = 1 + min(dp[r][c], dp[r][c + 1], dp[r + 1][c]); best = max(best, dp[r + 1][c + 1])
              return best * best
      """, hint="dp[r][c] = side of the largest square whose bottom-right corner is (r, c)."),
]

L_INTERVALS = [
    F("Summary Ranges", 228, "Easy", """
        `nums` is a sorted array of unique integers. Return the smallest sorted list of ranges covering exactly the same numbers. A range `[a, b]` is written `"a->b"` if `a != b`, and `"a"` if `a == b`.

        Constraints:
        - 0 <= nums.length <= 20
        """, "summaryRanges(nums:int[])->string[]",
      [([0, 1, 2, 4, 5, 7],), ([0, 2, 3, 4, 6, 8, 9],), ([],), ([1],), ([-1],), ([1, 3],), ([-3, -2, -1, 5],)],
      """
      class Solution:
          def summaryRanges(self, nums):
              res = []; i = 0
              while i < len(nums):
                  j = i
                  while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                      j += 1
                  res.append(str(nums[i]) if i == j else '%d->%d' % (nums[i], nums[j])); i = j + 1
              return res
      """, hint="Extend each run while the next number is exactly one more."),
    F("Minimum Number of Arrows to Burst Balloons", 452, "Medium", """
        Balloons are horizontal segments `points[i] = [xstart, xend]`. An arrow shot vertically at `x` bursts every balloon with `xstart <= x <= xend`. Return the minimum number of arrows needed to burst all balloons.

        Constraints:
        - 1 <= points.length <= 10^5
        """, "findMinArrowShots(points:int[][])->int",
      [([[10, 16], [2, 8], [1, 6], [7, 12]],), ([[1, 2], [3, 4], [5, 6], [7, 8]],), ([[1, 2], [2, 3], [3, 4], [4, 5]],), ([[1, 2]],), ([[-2147483646, -2147483645], [2147483646, 2147483647]],), ([[3, 9], [7, 12], [3, 8], [6, 8], [9, 10], [2, 9], [0, 9], [3, 9], [0, 6], [2, 8]],)],
      """
      class Solution:
          def findMinArrowShots(self, points):
              points.sort(key=lambda p: p[1]); arrows = 0; end = -float('inf')
              for s, e in points:
                  if s > end:
                      arrows += 1; end = e
              return arrows
      """, hint="Sort by end; shoot at the end of the first balloon and skip everything it bursts."),
]

L_MATRIX = [
    F("Game of Life", 289, "Medium", """
        Conway's Game of Life on an `m x n` board (1 = live, 0 = dead). Each cell looks at its 8 neighbours: a live cell with fewer than 2 or more than 3 live neighbours dies; a live cell with 2 or 3 survives; a dead cell with exactly 3 live neighbours becomes live. Compute the next state **in place**.

        Constraints:
        - 1 <= m, n <= 25
        """, "gameOfLife(board:int[][])->void",
      [([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]],), ([[1, 1], [1, 0]],), ([[1]],), ([[0]],), ([[1, 1, 1], [1, 1, 1], [1, 1, 1]],)],
      """
      class Solution:
          def gameOfLife(self, board):
              R, C = len(board), len(board[0])
              for r in range(R):
                  for c in range(C):
                      n = sum(board[a][b] & 1 for a in range(max(0, r - 1), min(R, r + 2)) for b in range(max(0, c - 1), min(C, c + 2))) - (board[r][c] & 1)
                      if (board[r][c] & 1 and n in (2, 3)) or (not board[r][c] & 1 and n == 3):
                          board[r][c] |= 2
              for r in range(R):
                  for c in range(C):
                      board[r][c] >>= 1
      """, inplace="board", hint="Encode the next state in the second bit so the original values stay readable while you scan."),
]

L_MATH = [
    F("Palindrome Number", 9, "Easy", """
        Return `true` if the integer `x` reads the same backwards and forwards. Negative numbers are never palindromes.

        Constraints:
        - -2^31 <= x <= 2^31 - 1
        """, "isPalindrome(x:int)->bool",
      [(121,), (-121,), (10,), (0,), (12321,), (1000021,)],
      """
      class Solution:
          def isPalindrome(self, x):
              return x >= 0 and str(x) == str(x)[::-1]
      """, hint="Try it without converting to a string by reversing half of the digits."),
    F("Factorial Trailing Zeroes", 172, "Medium", """
        Return the number of trailing zeroes in `n!`.

        Constraints:
        - 0 <= n <= 10^4
        """, "trailingZeroes(n:int)->int",
      [(3,), (5,), (0,), (25,), (100,), (10000,)],
      """
      class Solution:
          def trailingZeroes(self, n):
              c = 0
              while n:
                  n //= 5; c += n
              return c
      """, hint="Each trailing zero needs a factor 5 (there are always enough 2s)."),
    F("Sqrt(x)", 69, "Easy", """
        Return the integer part of the square root of the non-negative integer `x` (round down). Do not use a built-in power or square-root function.

        Constraints:
        - 0 <= x <= 2^31 - 1
        """, "mySqrt(x:int)->int",
      [(4,), (8,), (0,), (1,), (2147483647,), (2147395599,)],
      """
      class Solution:
          def mySqrt(self, x):
              l, r = 0, x
              while l < r:
                  m = (l + r + 1) // 2
                  if m * m <= x:
                      l = m
                  else:
                      r = m - 1
              return l
      """, hint="Binary search for the largest m with m * m <= x (watch for overflow in Java/C++: use long)."),
    F("Max Points on a Line", 149, "Hard", """
        Given distinct 2-D `points`, return the maximum number of points that lie on the same straight line.

        Constraints:
        - 1 <= points.length <= 300
        """, "maxPoints(points:int[][])->int",
      [([[1, 1], [2, 2], [3, 3]],), ([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]],), ([[0, 0]],), ([[0, 0], [1, 1]],), ([[0, 0], [1, 0], [2, 0], [0, 1]],), ([[2, 3], [3, 3], [-5, 3]],)],
      """
      class Solution:
          def maxPoints(self, points):
              n = len(points); best = min(n, 2)
              for i in range(n):
                  slopes = Counter()
                  for j in range(i + 1, n):
                      dx = points[j][0] - points[i][0]; dy = points[j][1] - points[i][1]
                      g = gcd(dx, dy); dx //= g; dy //= g
                      if dx < 0 or (dx == 0 and dy < 0):
                          dx, dy = -dx, -dy
                      slopes[(dx, dy)] += 1
                  if slopes:
                      best = max(best, max(slopes.values()) + 1)
              return best
      """, hint="For each point, count how many others share each (reduced) slope with it."),
]

L_BITS = [
    F("Add Binary", 67, "Easy", """
        Add two binary strings `a` and `b` and return their sum as a binary string.

        Constraints:
        - 1 <= a.length, b.length <= 10^4, no leading zeros except "0"
        """, "addBinary(a:string, b:string)->string",
      [("11", "1"), ("1010", "1011"), ("0", "0"), ("1", "111"), ("1111", "1111")],
      """
      class Solution:
          def addBinary(self, a, b):
              i, j, carry = len(a) - 1, len(b) - 1, 0; out = []
              while i >= 0 or j >= 0 or carry:
                  s = carry + (int(a[i]) if i >= 0 else 0) + (int(b[j]) if j >= 0 else 0)
                  out.append(str(s % 2)); carry = s // 2; i -= 1; j -= 1
              return ''.join(reversed(out))
      """, hint="Schoolbook addition from the right with a carry."),
    F("Single Number II", 137, "Medium", """
        Every element of `nums` appears exactly three times except one, which appears once. Return that single element using linear time and constant extra space.

        Constraints:
        - 1 <= nums.length <= 3 * 10^4
        """, "singleNumber(nums:int[])->int",
      [([2, 2, 3, 2],), ([0, 1, 0, 1, 0, 1, 99],), ([-2, -2, 1, 1, 4, 1, 4, 4, -4, -2],), ([5],), ([7, 7, 7, 8],)],
      """
      class Solution:
          def singleNumber(self, nums):
              ones = twos = 0
              for x in nums:
                  ones = (ones ^ x) & ~twos; twos = (twos ^ x) & ~ones
              return ones
      """, hint="Count each bit position modulo 3 (two accumulator variables do it)."),
    F("Bitwise AND of Numbers Range", 201, "Medium", """
        Return the bitwise AND of all integers in the inclusive range `[left, right]`.

        Constraints:
        - 0 <= left <= right <= 2^31 - 1
        """, "rangeBitwiseAnd(left:int, right:int)->int",
      [(5, 7), (0, 0), (1, 2147483647), (12, 15), (6, 7), (8, 8)],
      """
      class Solution:
          def rangeBitwiseAnd(self, left, right):
              shift = 0
              while left != right:
                  left >>= 1; right >>= 1; shift += 1
              return left << shift
      """, hint="The answer is the common binary prefix of left and right."),
]
