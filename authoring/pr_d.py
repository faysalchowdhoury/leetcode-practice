from dsl import F, D, R

def g(*rows):
    return [list(r) for r in rows]

INF = 2147483647

G16 = [
    F("Generate Parentheses", 22, "Medium", """
        Given `n` pairs of parentheses, return every well-formed combination. The order of the result does not matter.

        Constraints:
        - 1 <= n <= 8
        """, "generateParenthesis(n:int)->string[]",
      [(3,), (1,), (2,), (4,), (5,)],
      """
      class Solution:
          def generateParenthesis(self, n):
              res = []
              def go(s, o, c):
                  if len(s) == 2 * n:
                      res.append(s); return
                  if o < n: go(s + '(', o + 1, c)
                  if c < o: go(s + ')', o, c + 1)
              go('', 0, 0)
              return res
      """, cmp="sorted", hint="Add '(' while fewer than n are used; add ')' only while it would not exceed the opens."),
    F("Subsets", 78, "Medium", """
        Given an integer array `nums` of unique elements, return all possible subsets (the power set), without duplicates, in any order.

        Constraints:
        - 1 <= nums.length <= 10
        """, "subsets(nums:int[])->int[][]",
      [([1, 2, 3],), ([0],), ([1, 2],), ([4, 1, 0, 3],), ([-1, 5],)],
      """
      class Solution:
          def subsets(self, nums):
              res = [[]]
              for x in nums:
                  res += [s + [x] for s in res]
              return res
      """, cmp="sorted_deep", hint="For each element decide: include it or not."),
    F("Combination Sum", 39, "Medium", """
        Given distinct positive integers `candidates` and a `target`, return all unique combinations whose numbers sum to `target`. Each number may be used any number of times. Combinations may be returned in any order.

        Constraints:
        - 1 <= candidates.length <= 30, 2 <= candidates[i] <= 40, 1 <= target <= 40
        """, "combinationSum(candidates:int[], target:int)->int[][]",
      [([2, 3, 6, 7], 7), ([2, 3, 5], 8), ([2], 1), ([2, 3], 5), ([7, 3, 2], 18), ([3, 5, 8], 11)],
      """
      class Solution:
          def combinationSum(self, candidates, target):
              res = []
              def go(i, cur, rem):
                  if rem == 0:
                      res.append(cur[:]); return
                  if rem < 0 or i == len(candidates):
                      return
                  cur.append(candidates[i]); go(i, cur, rem - candidates[i]); cur.pop()
                  go(i + 1, cur, rem)
              go(0, [], target)
              return res
      """, cmp="sorted_deep", hint="At each index either take the number again (stay) or move on."),
    F("Combination Sum II", 40, "Medium", """
        Given `candidates` (which may contain duplicates) and a `target`, return all unique combinations that sum to `target`. Each number in `candidates` may be used at most once per combination. The result must not contain duplicate combinations.

        Constraints:
        - 1 <= candidates.length <= 100, 1 <= candidates[i] <= 50, 1 <= target <= 30
        """, "combinationSum2(candidates:int[], target:int)->int[][]",
      [([10, 1, 2, 7, 6, 1, 5], 8), ([2, 5, 2, 1, 2], 5), ([1], 1), ([2, 2, 2], 4), ([1, 1, 1, 1], 2), ([3, 1, 3, 5, 4, 1], 6)],
      """
      class Solution:
          def combinationSum2(self, candidates, target):
              candidates.sort(); res = []
              def go(start, cur, rem):
                  if rem == 0:
                      res.append(cur[:]); return
                  for i in range(start, len(candidates)):
                      if i > start and candidates[i] == candidates[i - 1]:
                          continue
                      if candidates[i] > rem:
                          break
                      cur.append(candidates[i]); go(i + 1, cur, rem - candidates[i]); cur.pop()
              go(0, [], target)
              return res
      """, cmp="sorted_deep", hint="Sort first and skip a value if it equals the previous one at the same recursion level."),
    F("Permutations", 46, "Medium", """
        Given an array `nums` of distinct integers, return all possible permutations in any order.

        Constraints:
        - 1 <= nums.length <= 6
        """, "permute(nums:int[])->int[][]",
      [([1, 2, 3],), ([0, 1],), ([1],), ([1, 2, 3, 4],), ([5, -2, 9],)],
      """
      class Solution:
          def permute(self, nums):
              return [list(p) for p in permutations(nums)]
      """, cmp="sorted", hint="Choose an unused element for position 0, then position 1, and so on."),
    F("Subsets II", 90, "Medium", """
        Given an integer array `nums` that may contain duplicates, return all possible subsets without duplicate subsets, in any order.

        Constraints:
        - 1 <= nums.length <= 10
        """, "subsetsWithDup(nums:int[])->int[][]",
      [([1, 2, 2],), ([0],), ([4, 4, 4, 1, 4],), ([1, 1, 2, 2],), ([2, 1, 2],)],
      """
      class Solution:
          def subsetsWithDup(self, nums):
              nums.sort(); res = []
              def go(i, cur):
                  res.append(cur[:])
                  for j in range(i, len(nums)):
                      if j > i and nums[j] == nums[j - 1]:
                          continue
                      cur.append(nums[j]); go(j + 1, cur); cur.pop()
              go(0, [])
              return res
      """, cmp="sorted_deep", hint="Sort, then skip equal values at the same depth."),
    F("Word Search", 79, "Medium", """
        Given an `m x n` grid of letters and a string `word`, return `true` if the word exists in the grid. The word is built from sequentially adjacent cells (horizontally or vertically), and a cell may be used at most once.

        Constraints:
        - 1 <= m, n <= 6, 1 <= word.length <= 15
        """, "exist(board:char[][], word:string)->bool",
      [(g("ABCE", "SFCS", "ADEE"), "ABCCED"), (g("ABCE", "SFCS", "ADEE"), "SEE"), (g("ABCE", "SFCS", "ADEE"), "ABCB"), (g("a"), "a"), (g("ab", "cd"), "abdc"), (g("aa"), "aaa")],
      """
      class Solution:
          def exist(self, board, word):
              R, C = len(board), len(board[0])
              def dfs(r, c, i):
                  if i == len(word):
                      return True
                  if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[i]:
                      return False
                  t = board[r][c]; board[r][c] = '#'
                  ok = dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1)
                  board[r][c] = t
                  return ok
              return any(dfs(r, c, 0) for r in range(R) for c in range(C))
      """, hint="DFS from each cell, marking visited cells and un-marking when you backtrack."),
    F("Palindrome Partitioning", 131, "Medium", """
        Partition string `s` so that every substring of the partition is a palindrome. Return all possible partitions in any order.

        Constraints:
        - 1 <= s.length <= 16, lowercase English letters
        """, "partition(s:string)->string[][]",
      [("aab",), ("a",), ("aba",), ("abbab",), ("aaaa",)],
      """
      class Solution:
          def partition(self, s):
              res = []
              def go(i, cur):
                  if i == len(s):
                      res.append(cur[:]); return
                  for j in range(i + 1, len(s) + 1):
                      t = s[i:j]
                      if t == t[::-1]:
                          cur.append(t); go(j, cur); cur.pop()
              go(0, [])
              return res
      """, cmp="sorted", hint="Try every prefix that is a palindrome, then partition the rest."),
    F("Letter Combinations of a Phone Number", 17, "Medium", """
        Given a string of digits `2-9`, return all letter combinations it could represent on a phone keypad (2=abc, 3=def, 4=ghi, 5=jkl, 6=mno, 7=pqrs, 8=tuv, 9=wxyz). Return an empty list for an empty string.

        Constraints:
        - 0 <= digits.length <= 4
        """, "letterCombinations(digits:string)->string[]",
      [("23",), ("",), ("2",), ("79",), ("234",)],
      """
      class Solution:
          def letterCombinations(self, digits):
              if not digits:
                  return []
              m = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
              res = ['']
              for d in digits:
                  res = [p + c for p in res for c in m[d]]
              return res
      """, cmp="sorted", hint="Build the answer one digit at a time."),
    F("N-Queens", 51, "Hard", """
        Place `n` queens on an `n x n` board so that no two attack each other. Return every distinct solution as a list of board layouts, using `'Q'` for a queen and `'.'` for an empty square. Solutions may be in any order.

        Constraints:
        - 1 <= n <= 9
        """, "solveNQueens(n:int)->string[][]",
      [(4,), (1,), (5,), (3,), (6,)],
      """
      class Solution:
          def solveNQueens(self, n):
              res = []; cols = set(); d1 = set(); d2 = set(); pos = []
              def go(r):
                  if r == n:
                      res.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in pos]); return
                  for c in range(n):
                      if c in cols or r - c in d1 or r + c in d2:
                          continue
                      cols.add(c); d1.add(r - c); d2.add(r + c); pos.append(c)
                      go(r + 1)
                      cols.remove(c); d1.remove(r - c); d2.remove(r + c); pos.pop()
              go(0)
              return res
      """, cmp="sorted", hint="Place one queen per row; track used columns and both diagonals in sets."),
]

G17 = [
    F("Number of Islands", 200, "Medium", """
        Given a grid of `'1'` (land) and `'0'` (water), return the number of islands. An island is a group of land cells connected horizontally or vertically.

        Constraints:
        - 1 <= m, n <= 300
        """, "numIslands(grid:char[][])->int",
      [(g("11110", "11010", "11000", "00000"),), (g("11000", "11000", "00100", "00011"),), (g("0"),), (g("1"),), (g("101", "010", "101"),), (g("111", "010", "111"),)],
      """
      class Solution:
          def numIslands(self, grid):
              R, C = len(grid), len(grid[0]); n = 0
              def sink(r, c):
                  st = [(r, c)]; grid[r][c] = '0'
                  while st:
                      x, y = st.pop()
                      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                          a, b = x + dx, y + dy
                          if 0 <= a < R and 0 <= b < C and grid[a][b] == '1':
                              grid[a][b] = '0'; st.append((a, b))
              for r in range(R):
                  for c in range(C):
                      if grid[r][c] == '1':
                          n += 1; sink(r, c)
              return n
      """, hint="Each time you find unvisited land, count one island and flood-fill it."),
    F("Max Area of Island", 695, "Medium", """
        Given a binary grid, return the area (number of cells) of the largest island of 1s, where cells are connected horizontally or vertically. Return 0 if there is no island.

        Constraints:
        - 1 <= m, n <= 50
        """, "maxAreaOfIsland(grid:int[][])->int",
      [([[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]],), ([[0, 0, 0, 0, 0, 0, 0, 0]],), ([[1]],), ([[1, 1], [1, 1]],), ([[1, 0, 1], [1, 1, 0]],)],
      """
      class Solution:
          def maxAreaOfIsland(self, grid):
              R, C = len(grid), len(grid[0]); best = 0
              def area(r, c):
                  if not (0 <= r < R and 0 <= c < C) or grid[r][c] != 1:
                      return 0
                  grid[r][c] = 0
                  return 1 + area(r + 1, c) + area(r - 1, c) + area(r, c + 1) + area(r, c - 1)
              for r in range(R):
                  for c in range(C):
                      best = max(best, area(r, c))
              return best
      """, hint="DFS returns the size of the island it floods."),
    F("Clone Graph", 133, "Medium", """
        Given a reference to a node in a connected undirected graph, return a deep copy of the graph. Each node has an integer `val` and a list `neighbors`.

        In the tests the graph is shown as an adjacency list: node `i` (1-indexed, with `val = i`) has neighbors `adj[i-1]`. The first node you receive is node 1; an empty list means a null graph.

        Constraints:
        - 0 <= number of nodes <= 100, 1 <= Node.val <= 100, values unique
        """, "cloneGraph(node:Node)->Node",
      [([[2, 4], [1, 3], [2, 4], [1, 3]],), ([[]],), ([],), ([[2], [1]],), ([[2, 3], [1, 3], [1, 2]],), ([[2, 5], [1, 3], [2, 4], [3, 5], [4, 1]],)],
      """
      class Solution:
          def cloneGraph(self, node):
              if not node:
                  return None
              m = {node: Node(node.val)}; q = deque([node])
              while q:
                  n = q.popleft()
                  for nb in n.neighbors:
                      if nb not in m:
                          m[nb] = Node(nb.val); q.append(nb)
                      m[n].neighbors.append(m[nb])
              return m[node]
      """, hint="Map original node -> copy; create copies lazily while traversing."),
    F("Walls and Gates", 286, "Medium", """
        You are given an `m x n` grid `rooms` with these values: `-1` is a wall, `0` is a gate, and `2147483647` (INF) is an empty room. Fill each empty room with the distance to its nearest gate (moving up, down, left or right). Rooms that cannot reach a gate stay INF. Modify the grid in place.

        Constraints:
        - 1 <= m, n <= 250
        """, "wallsAndGates(rooms:int[][])->void",
      [([[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]],), ([[0]],), ([[INF]],), ([[INF, 0]],), ([[0, INF, INF], [INF, -1, INF], [INF, INF, 0]],), ([[INF, -1], [-1, 0]],)],
      """
      class Solution:
          def wallsAndGates(self, rooms):
              R, C = len(rooms), len(rooms[0])
              q = deque((r, c) for r in range(R) for c in range(C) if rooms[r][c] == 0)
              while q:
                  r, c = q.popleft()
                  for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                      a, b = r + dr, c + dc
                      if 0 <= a < R and 0 <= b < C and rooms[a][b] == 2147483647:
                          rooms[a][b] = rooms[r][c] + 1; q.append((a, b))
      """, inplace="rooms", hint="Multi-source BFS starting from every gate at once."),
    F("Rotting Oranges", 994, "Medium", """
        In a grid, `0` is empty, `1` is a fresh orange and `2` is a rotten orange. Every minute, each fresh orange next to a rotten one (up, down, left, right) becomes rotten. Return the minimum number of minutes until no fresh orange remains, or -1 if that is impossible.

        Constraints:
        - 1 <= m, n <= 10
        """, "orangesRotting(grid:int[][])->int",
      [([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), ([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), ([[0, 2]],), ([[0]],), ([[1]],), ([[2], [1], [1], [1], [2], [1], [1]],)],
      """
      class Solution:
          def orangesRotting(self, grid):
              R, C = len(grid), len(grid[0]); q = deque(); fresh = 0
              for r in range(R):
                  for c in range(C):
                      if grid[r][c] == 2: q.append((r, c))
                      elif grid[r][c] == 1: fresh += 1
              t = 0
              while q and fresh:
                  t += 1
                  for _ in range(len(q)):
                      r, c = q.popleft()
                      for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                          a, b = r + dr, c + dc
                          if 0 <= a < R and 0 <= b < C and grid[a][b] == 1:
                              grid[a][b] = 2; fresh -= 1; q.append((a, b))
              return -1 if fresh else t
      """, hint="BFS by levels from all rotten oranges; each level is one minute."),
    F("Pacific Atlantic Water Flow", 417, "Medium", """
        `heights[r][c]` is the height of a cell. Water flows from a cell to a neighbouring cell with height less than or equal to it. The Pacific Ocean touches the top and left edges and the Atlantic touches the bottom and right edges.

        Return all coordinates `[r, c]` from which water can flow to both oceans, in any order.

        Constraints:
        - 1 <= m, n <= 200
        """, "pacificAtlantic(heights:int[][])->int[][]",
      [([[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]],), ([[1]],), ([[1, 1], [1, 1], [1, 1]],), ([[2, 1], [1, 2]],), ([[3, 3, 3], [3, 1, 3], [0, 2, 4]],)],
      """
      class Solution:
          def pacificAtlantic(self, heights):
              R, C = len(heights), len(heights[0])
              def fill(starts):
                  seen = set(starts); st = list(starts)
                  while st:
                      r, c = st.pop()
                      for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                          a, b = r + dr, c + dc
                          if 0 <= a < R and 0 <= b < C and (a, b) not in seen and heights[a][b] >= heights[r][c]:
                              seen.add((a, b)); st.append((a, b))
                  return seen
              pac = fill([(0, c) for c in range(C)] + [(r, 0) for r in range(R)])
              atl = fill([(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R)])
              return [list(p) for p in pac & atl]
      """, cmp="sorted", hint="Search backwards from each ocean (uphill) and intersect the two reachable sets."),
    F("Surrounded Regions", 130, "Medium", """
        A board contains `'X'` and `'O'`. Capture every region of `'O'` cells that is completely surrounded by `'X'` (regions touching the border are not captured) by flipping all its `'O'` to `'X'`. Modify the board in place.

        Constraints:
        - 1 <= m, n <= 200
        """, "solve(board:char[][])->void",
      [(g("XXXX", "XOOX", "XXOX", "XOXX"),), (g("X"),), (g("O"),), (g("OO", "OO"),), (g("XOX", "OXO", "XOX"),), (g("XXXXX", "XOOOX", "XOXOX", "XOOOX", "XXXXX"),)],
      """
      class Solution:
          def solve(self, board):
              R, C = len(board), len(board[0])
              st = [(r, c) for r in range(R) for c in range(C) if (r in (0, R - 1) or c in (0, C - 1)) and board[r][c] == 'O']
              for r, c in st:
                  board[r][c] = 'S'
              while st:
                  r, c = st.pop()
                  for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                      a, b = r + dr, c + dc
                      if 0 <= a < R and 0 <= b < C and board[a][b] == 'O':
                          board[a][b] = 'S'; st.append((a, b))
              for r in range(R):
                  for c in range(C):
                      board[r][c] = 'O' if board[r][c] == 'S' else 'X'
      """, inplace="board", hint="Mark every O reachable from the border as safe first, then flip whatever is left."),
    F("Word Ladder", 127, "Hard", """
        Transform `beginWord` into `endWord` by changing one letter at a time, where each intermediate word must be in `wordList`. Return the number of words in the shortest transformation sequence (counting both ends), or 0 if none exists. `beginWord` itself need not be in the list.

        Constraints:
        - 1 <= beginWord.length <= 10, all words have the same length, lowercase letters
        - 1 <= wordList.length <= 5000
        """, "ladderLength(beginWord:string, endWord:string, wordList:string[])->int",
      [("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), ("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), ("a", "c", ["a", "b", "c"]), ("hot", "dog", ["hot", "dog"]), ("lost", "cost", ["most", "fist", "lost", "cost", "fish"]), ("red", "tax", ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"])],
      """
      class Solution:
          def ladderLength(self, beginWord, endWord, wordList):
              words = set(wordList)
              if endWord not in words:
                  return 0
              q = deque([(beginWord, 1)]); seen = {beginWord}
              while q:
                  w, d = q.popleft()
                  if w == endWord:
                      return d
                  for i in range(len(w)):
                      for ch in 'abcdefghijklmnopqrstuvwxyz':
                          x = w[:i] + ch + w[i + 1:]
                          if x in words and x not in seen:
                              seen.add(x); q.append((x, d + 1))
              return 0
      """, hint="BFS over words; neighbours differ in exactly one letter."),
]

G18 = [
    F("Course Schedule", 207, "Medium", """
        There are `numCourses` courses labelled `0..numCourses-1`. `prerequisites[i] = [a, b]` means you must take course `b` before course `a`. Return `true` if you can finish all courses (the prerequisite graph has no cycle).

        Constraints:
        - 1 <= numCourses <= 2000
        - 0 <= prerequisites.length <= 5000
        """, "canFinish(numCourses:int, prerequisites:int[][])->bool",
      [(2, [[1, 0]]), (2, [[1, 0], [0, 1]]), (1, []), (4, [[1, 0], [2, 1], [3, 2]]), (3, [[0, 1], [1, 2], [2, 0]]), (5, [[1, 4], [2, 4], [3, 1], [3, 2]])],
      """
      class Solution:
          def canFinish(self, numCourses, prerequisites):
              adj = defaultdict(list); indeg = [0] * numCourses
              for a, b in prerequisites:
                  adj[b].append(a); indeg[a] += 1
              q = deque(i for i in range(numCourses) if not indeg[i]); done = 0
              while q:
                  x = q.popleft(); done += 1
                  for y in adj[x]:
                      indeg[y] -= 1
                      if not indeg[y]:
                          q.append(y)
              return done == numCourses
      """, hint="Kahn's algorithm: repeatedly take courses with no remaining prerequisites."),
    F("Course Schedule II", 210, "Medium", """
        Same input as Course Schedule. Return **an** ordering of courses that satisfies all prerequisites. If several orderings are valid, return any of them; if it is impossible, return an empty array.

        Constraints:
        - 1 <= numCourses <= 2000
        """, "findOrder(numCourses:int, prerequisites:int[][])->int[]",
      [(2, [[1, 0]]), (4, [[1, 0], [2, 0], [3, 1], [3, 2]]), (1, []), (2, [[1, 0], [0, 1]]), (3, []), (3, [[1, 0], [2, 1]])],
      """
      class Solution:
          def findOrder(self, numCourses, prerequisites):
              adj = defaultdict(list); indeg = [0] * numCourses
              for a, b in prerequisites:
                  adj[b].append(a); indeg[a] += 1
              q = deque(i for i in range(numCourses) if not indeg[i]); order = []
              while q:
                  x = q.popleft(); order.append(x)
                  for y in adj[x]:
                      indeg[y] -= 1
                      if not indeg[y]:
                          q.append(y)
              return order if len(order) == numCourses else []
      """, cmp="topo", hint="The same topological sort, but record the order."),
    F("Alien Dictionary", 269, "Hard", """
        An alien language uses the lowercase English letters in an unknown order. `words` is sorted lexicographically according to that order. Return a string containing every letter that appears in `words`, in a valid order of the alien alphabet. If several orders are valid return any; if the input is inconsistent (including a longer word placed before its own prefix) return `""`.

        Constraints:
        - 1 <= words.length <= 100, 1 <= words[i].length <= 100
        """, "alienOrder(words:string[])->string",
      [(["wrt", "wrf", "er", "ett", "rftt"],), (["z", "x"],), (["z", "x", "z"],), (["abc", "ab"],), (["a"],), (["ba", "bc", "ac", "cab"],)],
      """
      class Solution:
          def alienOrder(self, words):
              adj = {c: set() for w in words for c in w}
              for a, b in zip(words, words[1:]):
                  m = min(len(a), len(b))
                  if len(a) > len(b) and a[:m] == b[:m]:
                      return ""
                  for i in range(m):
                      if a[i] != b[i]:
                          adj[a[i]].add(b[i]); break
              indeg = {c: 0 for c in adj}
              for c in adj:
                  for d in adj[c]:
                      indeg[d] += 1
              q = deque(c for c in adj if indeg[c] == 0); out = []
              while q:
                  c = q.popleft(); out.append(c)
                  for d in adj[c]:
                      indeg[d] -= 1
                      if indeg[d] == 0:
                          q.append(d)
              return ''.join(out) if len(out) == len(adj) else ""
      """, cmp="alien", hint="Compare each adjacent pair of words to find one letter ordering, then topologically sort the letters."),
]

G19 = [
    F("Redundant Connection", 684, "Medium", """
        A tree with `n` nodes (labelled `1..n`) had one extra edge added, creating exactly one cycle. `edges[i] = [a, b]`. Return an edge that can be removed so the graph becomes a tree. If there are several answers, return the one that occurs last in the input.

        Constraints:
        - 3 <= n <= 1000
        """, "findRedundantConnection(edges:int[][])->int[]",
      [([[1, 2], [1, 3], [2, 3]],), ([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],), ([[1, 2], [2, 3], [1, 3], [3, 4]],), ([[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]],), ([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]],)],
      """
      class Solution:
          def findRedundantConnection(self, edges):
              p = list(range(len(edges) + 1))
              def find(x):
                  while p[x] != x:
                      p[x] = p[p[x]]; x = p[x]
                  return x
              for a, b in edges:
                  ra, rb = find(a), find(b)
                  if ra == rb:
                      return [a, b]
                  p[ra] = rb
      """, hint="Union-Find: the first edge whose endpoints are already connected closes the cycle."),
    F("Number of Connected Components in an Undirected Graph", 323, "Medium", """
        There are `n` nodes labelled `0..n-1` and a list of undirected `edges`. Return the number of connected components.

        Constraints:
        - 1 <= n <= 2000
        """, "countComponents(n:int, edges:int[][])->int",
      [(5, [[0, 1], [1, 2], [3, 4]]), (5, [[0, 1], [1, 2], [2, 3], [3, 4]]), (1, []), (4, []), (6, [[0, 1], [2, 3], [4, 5], [1, 2]]), (3, [[0, 1], [1, 0]])],
      """
      class Solution:
          def countComponents(self, n, edges):
              p = list(range(n))
              def find(x):
                  while p[x] != x:
                      p[x] = p[p[x]]; x = p[x]
                  return x
              c = n
              for a, b in edges:
                  ra, rb = find(a), find(b)
                  if ra != rb:
                      p[ra] = rb; c -= 1
              return c
      """, hint="Start with n components; each successful union reduces the count by one."),
    F("Graph Valid Tree", 261, "Medium", """
        Given `n` nodes labelled `0..n-1` and a list of undirected `edges`, return `true` if the edges make up a valid tree (connected and with no cycle).

        Constraints:
        - 1 <= n <= 2000
        """, "validTree(n:int, edges:int[][])->bool",
      [(5, [[0, 1], [0, 2], [0, 3], [1, 4]]), (5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]), (1, []), (2, []), (4, [[0, 1], [2, 3]]), (3, [[0, 1], [1, 2], [2, 0]])],
      """
      class Solution:
          def validTree(self, n, edges):
              if len(edges) != n - 1:
                  return False
              p = list(range(n))
              def find(x):
                  while p[x] != x:
                      p[x] = p[p[x]]; x = p[x]
                  return x
              for a, b in edges:
                  ra, rb = find(a), find(b)
                  if ra == rb:
                      return False
                  p[ra] = rb
              return True
      """, hint="A tree on n nodes has exactly n - 1 edges and no cycle."),
]

G20 = [
    F("Network Delay Time", 743, "Medium", """
        `times[i] = [u, v, w]` is a directed edge from `u` to `v` taking `w` time. A signal is sent from node `k`. Return the minimum time for all `n` nodes (labelled `1..n`) to receive it, or -1 if some node can never receive it.

        Constraints:
        - 1 <= k <= n <= 100, 1 <= times.length <= 6000, 0 <= w <= 100
        """, "networkDelayTime(times:int[][], n:int, k:int)->int",
      [([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), ([[1, 2, 1]], 2, 1), ([[1, 2, 1]], 2, 2), ([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1), ([[1, 2, 1], [2, 1, 3]], 2, 2)],
      """
      class Solution:
          def networkDelayTime(self, times, n, k):
              adj = defaultdict(list)
              for u, v, w in times:
                  adj[u].append((v, w))
              dist = {}; h = [(0, k)]
              while h:
                  d, u = heappop(h)
                  if u in dist:
                      continue
                  dist[u] = d
                  for v, w in adj[u]:
                      if v not in dist:
                          heappush(h, (d + w, v))
              return max(dist.values()) if len(dist) == n else -1
      """, hint="Dijkstra from k; the answer is the largest shortest distance."),
    F("Swim in Rising Water", 778, "Hard", """
        In an `n x n` grid, `grid[r][c]` is the elevation. At time `t` the water level is `t`, and you can swim between adjacent cells only if both elevations are at most `t`. Starting at the top-left, return the least time `t` at which you can reach the bottom-right.

        Constraints:
        - 1 <= n <= 50, grid contains a permutation of 0..n*n-1
        """, "swimInWater(grid:int[][])->int",
      [([[0, 2], [1, 3]],), ([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]],), ([[0]],), ([[3, 2], [0, 1]],), ([[0, 3, 4], [1, 2, 5], [8, 7, 6]],)],
      """
      class Solution:
          def swimInWater(self, grid):
              n = len(grid); h = [(grid[0][0], 0, 0)]; seen = {(0, 0)}
              while h:
                  t, r, c = heappop(h)
                  if (r, c) == (n - 1, n - 1):
                      return t
                  for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                      a, b = r + dr, c + dc
                      if 0 <= a < n and 0 <= b < n and (a, b) not in seen:
                          seen.add((a, b)); heappush(h, (max(t, grid[a][b]), a, b))
      """, hint="Dijkstra where the cost of a path is the maximum elevation along it."),
    F("Cheapest Flights Within K Stops", 787, "Medium", """
        There are `n` cities and `flights[i] = [from, to, price]`. Return the cheapest price from `src` to `dst` using at most `k` stops (so at most `k + 1` flights), or -1 if no such route exists.

        Constraints:
        - 1 <= n <= 100, 0 <= k < n
        """, "findCheapestPrice(n:int, flights:int[][], src:int, dst:int, k:int)->int",
      [(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1), (3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1), (3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0), (4, [[0, 1, 1], [0, 2, 5], [1, 2, 1], [2, 3, 1]], 0, 3, 1), (2, [], 0, 1, 1), (5, [[0, 1, 5], [1, 2, 5], [0, 3, 2], [3, 1, 2], [1, 4, 1], [4, 2, 1]], 0, 2, 2)],
      """
      class Solution:
          def findCheapestPrice(self, n, flights, src, dst, k):
              INF = float('inf'); dist = [INF] * n; dist[src] = 0
              for _ in range(k + 1):
                  nd = dist[:]
                  for u, v, w in flights:
                      if dist[u] + w < nd[v]:
                          nd[v] = dist[u] + w
                  dist = nd
              return -1 if dist[dst] == INF else dist[dst]
      """, hint="Bellman-Ford limited to k + 1 rounds, relaxing from the previous round's distances."),
]

G21 = [
    F("Min Cost to Connect All Points", 1584, "Medium", """
        `points[i] = [x, y]`. The cost to connect two points is their Manhattan distance `|x1 - x2| + |y1 - y2|`. Return the minimum total cost to connect all points so that there is exactly one simple path between any two of them.

        Constraints:
        - 1 <= points.length <= 1000
        """, "minCostConnectPoints(points:int[][])->int",
      [([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]],), ([[3, 12], [-2, 5], [-4, 1]],), ([[0, 0]],), ([[0, 0], [1, 1]],), ([[0, 0], [1, 1], [1, 0], [-1, 1]],)],
      """
      class Solution:
          def minCostConnectPoints(self, points):
              n = len(points); INF = float('inf'); d = [INF] * n; d[0] = 0; used = [False] * n; total = 0
              for _ in range(n):
                  u = min((i for i in range(n) if not used[i]), key=lambda i: d[i])
                  used[u] = True; total += d[u]
                  for v in range(n):
                      if not used[v]:
                          d[v] = min(d[v], abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1]))
              return total
      """, hint="Minimum spanning tree: Prim's or Kruskal's algorithm."),
    F("Reconstruct Itinerary", 332, "Hard", """
        `tickets[i] = [from, to]` are airline tickets. Reconstruct the itinerary in order, starting from `"JFK"`, using every ticket exactly once. If several itineraries exist, return the one that is smallest in lexical order. A valid itinerary is guaranteed to exist.

        Constraints:
        - 1 <= tickets.length <= 300
        - airports are 3 uppercase letters
        """, "findItinerary(tickets:string[][])->string[]",
      [([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]],), ([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]],), ([["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]],), ([["JFK", "AAA"]],), ([["JFK", "AAA"], ["AAA", "JFK"], ["JFK", "BBB"]],)],
      """
      class Solution:
          def findItinerary(self, tickets):
              adj = defaultdict(list)
              for a, b in sorted(tickets, reverse=True):
                  adj[a].append(b)
              res = []
              def go(a):
                  while adj[a]:
                      go(adj[a].pop())
                  res.append(a)
              go('JFK')
              return res[::-1]
      """, hint="Hierholzer's algorithm for an Eulerian path, visiting destinations in lexical order."),
]
