from dsl import F, D, R

def g(*rows):
    return [list(r) for r in rows]

G22 = [
    F("Climbing Stairs", 70, "Easy", """
        You are climbing a staircase of `n` steps. Each move climbs 1 or 2 steps. Return the number of distinct ways to reach the top.

        Constraints:
        - 1 <= n <= 45
        """, "climbStairs(n:int)->int",
      [(2,), (3,), (1,), (5,), (10,), (30,), (45,)],
      """
      class Solution:
          def climbStairs(self, n):
              a, b = 1, 1
              for _ in range(n - 1):
                  a, b = b, a + b
              return b
      """, hint="ways(n) = ways(n-1) + ways(n-2)."),
    F("Min Cost Climbing Stairs", 746, "Easy", """
        `cost[i]` is the price to step off stair `i` (climbing one or two stairs). You may start on stair 0 or 1. Return the minimum cost to reach the top, which is one step beyond the last stair.

        Constraints:
        - 2 <= cost.length <= 1000, 0 <= cost[i] <= 999
        """, "minCostClimbingStairs(cost:int[])->int",
      [([10, 15, 20],), ([1, 100, 1, 1, 1, 100, 1, 1, 100, 1],), ([5, 5],), ([0, 0, 0, 0],), ([1, 2, 3],), ([20, 15, 30, 5],)],
      """
      class Solution:
          def minCostClimbingStairs(self, cost):
              a, b = 0, 0
              for i in range(2, len(cost) + 1):
                  a, b = b, min(b + cost[i - 1], a + cost[i - 2])
              return b
      """, hint="best[i] = min(best[i-1] + cost[i-1], best[i-2] + cost[i-2])."),
    F("House Robber", 198, "Medium", """
        Houses lie in a row and `nums[i]` is the money in house `i`. You cannot rob two adjacent houses. Return the maximum amount you can rob.

        Constraints:
        - 1 <= nums.length <= 100, 0 <= nums[i] <= 400
        """, "rob(nums:int[])->int",
      [([1, 2, 3, 1],), ([2, 7, 9, 3, 1],), ([5],), ([2, 1],), ([1, 3, 1, 3, 100],), ([0, 0, 0],)],
      """
      class Solution:
          def rob(self, nums):
              a = b = 0
              for x in nums:
                  a, b = b, max(b, a + x)
              return b
      """, hint="At each house: skip it, or rob it plus the best from two houses back."),
    F("House Robber II", 213, "Medium", """
        Same as House Robber, but the houses are arranged in a **circle**, so the first and last houses are adjacent. Return the maximum amount you can rob.

        Constraints:
        - 1 <= nums.length <= 100, 0 <= nums[i] <= 1000
        """, "rob(nums:int[])->int",
      [([2, 3, 2],), ([1, 2, 3, 1],), ([1, 2, 3],), ([1],), ([200, 3, 140, 20, 10],), ([1, 1, 1, 2],)],
      """
      class Solution:
          def rob(self, nums):
              def line(a):
                  x = y = 0
                  for v in a:
                      x, y = y, max(y, x + v)
                  return y
              return nums[0] if len(nums) == 1 else max(line(nums[1:]), line(nums[:-1]))
      """, hint="Run House Robber twice: once without the first house, once without the last."),
    F("Decode Ways", 91, "Medium", """
        A message of digits encodes letters with `'A'=1, 'B'=2, ..., 'Z'=26`. Given a digit string `s`, return the number of ways to decode it. A leading zero cannot be decoded on its own. Return 0 if no decoding exists.

        Constraints:
        - 1 <= s.length <= 100
        """, "numDecodings(s:string)->int",
      [("12",), ("226",), ("06",), ("0",), ("10",), ("2101",), ("11106",), ("1" * 40,)],
      """
      class Solution:
          def numDecodings(self, s):
              a, b = 0, 1
              for i, ch in enumerate(s):
                  cur = 0
                  if ch != '0':
                      cur += b
                  if i and 10 <= int(s[i - 1:i + 1]) <= 26:
                      cur += a
                  a, b = b, cur
              return b
      """, hint="dp[i] adds dp[i-1] for a valid single digit and dp[i-2] for a valid two-digit number."),
    F("Coin Change", 322, "Medium", """
        Given coin denominations `coins` (unlimited supply of each) and a total `amount`, return the fewest coins needed to make that amount, or -1 if it cannot be made.

        Constraints:
        - 1 <= coins.length <= 12, 0 <= amount <= 10^4
        """, "coinChange(coins:int[], amount:int)->int",
      [([1, 2, 5], 11), ([2], 3), ([1], 0), ([186, 419, 83, 408], 6249), ([2, 5, 10, 1], 27), ([3, 7], 11), ([1, 3, 4], 6)],
      """
      class Solution:
          def coinChange(self, coins, amount):
              INF = amount + 1; dp = [0] + [INF] * amount
              for a in range(1, amount + 1):
                  for c in coins:
                      if c <= a:
                          dp[a] = min(dp[a], dp[a - c] + 1)
              return -1 if dp[amount] >= INF else dp[amount]
      """, hint="dp[a] = 1 + min(dp[a - coin]) over all coins."),
    F("Maximum Product Subarray", 152, "Medium", """
        Return the largest product of any contiguous non-empty subarray of `nums`.

        Constraints:
        - 1 <= nums.length <= 2 * 10^4, the answer fits in a 32-bit integer
        """, "maxProduct(nums:int[])->int",
      [([2, 3, -2, 4],), ([-2, 0, -1],), ([-2],), ([-2, 3, -4],), ([0, 2],), ([2, -5, -2, -4, 3],)],
      """
      class Solution:
          def maxProduct(self, nums):
              hi = lo = best = nums[0]
              for x in nums[1:]:
                  c = (x, hi * x, lo * x)
                  hi, lo = max(c), min(c); best = max(best, hi)
              return best
      """, hint="Track both the max and the min product ending here, since a negative can flip them."),
    F("Word Break", 139, "Medium", """
        Given a string `s` and a list `wordDict`, return `true` if `s` can be split into a sequence of dictionary words (words may be reused).

        Constraints:
        - 1 <= s.length <= 300, 1 <= wordDict.length <= 1000
        """, "wordBreak(s:string, wordDict:string[])->bool",
      [("leetcode", ["leet", "code"]), ("applepenapple", ["apple", "pen"]), ("catsandog", ["cats", "dog", "sand", "and", "cat"]), ("a", ["b"]), ("aaaaaaa", ["aaaa", "aaa"]), ("cars", ["car", "ca", "rs"]), ("a" * 60 + "b", ["a", "aa", "aaa", "aaaa"])],
      """
      class Solution:
          def wordBreak(self, s, wordDict):
              words = set(wordDict); dp = [True] + [False] * len(s)
              for i in range(1, len(s) + 1):
                  dp[i] = any(dp[j] and s[j:i] in words for j in range(i))
              return dp[-1]
      """, hint="dp[i] is true if some earlier dp[j] is true and s[j:i] is a word."),
    F("Longest Increasing Subsequence", 300, "Medium", """
        Return the length of the longest strictly increasing subsequence of `nums` (elements need not be adjacent).

        Constraints:
        - 1 <= nums.length <= 2500
        """, "lengthOfLIS(nums:int[])->int",
      [([10, 9, 2, 5, 3, 7, 101, 18],), ([0, 1, 0, 3, 2, 3],), ([7, 7, 7, 7],), ([1],), ([4, 10, 4, 3, 8, 9],), ([5, 4, 3, 2, 1],)],
      """
      class Solution:
          def lengthOfLIS(self, nums):
              tails = []
              for x in nums:
                  i = bisect_left(tails, x)
                  if i == len(tails):
                      tails.append(x)
                  else:
                      tails[i] = x
              return len(tails)
      """, hint="O(n^2) dp works; for O(n log n) keep the smallest tail of each length and binary search."),
    F("Partition Equal Subset Sum", 416, "Medium", """
        Return `true` if `nums` can be split into two subsets with equal sums.

        Constraints:
        - 1 <= nums.length <= 200, 1 <= nums[i] <= 100
        """, "canPartition(nums:int[])->bool",
      [([1, 5, 11, 5],), ([1, 2, 3, 5],), ([1, 1],), ([2, 2, 3, 5],), ([100],), ([1, 2, 5],), ([3, 3, 3, 4, 5],)],
      """
      class Solution:
          def canPartition(self, nums):
              s = sum(nums)
              if s % 2:
                  return False
              dp = 1
              for x in nums:
                  dp |= dp << x
              return bool((dp >> (s // 2)) & 1)
      """, hint="Subset-sum: can some subset reach total/2?"),
]

G23 = [
    F("Longest Palindromic Substring", 5, "Medium", """
        Return the longest palindromic substring of `s`. If several have the same length, any one of them is accepted.

        Constraints:
        - 1 <= s.length <= 1000
        """, "longestPalindrome(s:string)->string",
      [("babad",), ("cbbd",), ("a",), ("ac",), ("forgeeksskeegfor",), ("abacdfgdcaba",), ("a" * 200 + "b" + "a" * 100,)],
      """
      class Solution:
          def longestPalindrome(self, s):
              best = ''
              for c in range(len(s)):
                  for l, r in ((c, c), (c, c + 1)):
                      while l >= 0 and r < len(s) and s[l] == s[r]:
                          l -= 1; r += 1
                      if r - l - 1 > len(best):
                          best = s[l + 1:r]
              return best
      """, cmp="palsub", hint="Expand around every center (odd and even length)."),
    F("Palindromic Substrings", 647, "Medium", """
        Return the number of palindromic substrings of `s`. Substrings at different positions count separately even if they look identical.

        Constraints:
        - 1 <= s.length <= 1000
        """, "countSubstrings(s:string)->int",
      [("abc",), ("aaa",), ("a",), ("abba",), ("racecar",), ("a" * 300,)],
      """
      class Solution:
          def countSubstrings(self, s):
              n = 0
              for c in range(len(s)):
                  for l, r in ((c, c), (c, c + 1)):
                      while l >= 0 and r < len(s) and s[l] == s[r]:
                          n += 1; l -= 1; r += 1
              return n
      """, hint="Same center expansion; count every successful expansion."),
]

G24 = [
    F("Unique Paths", 62, "Medium", """
        A robot starts at the top-left of an `m x n` grid and can only move right or down. Return the number of distinct paths to the bottom-right corner.

        Constraints:
        - 1 <= m, n <= 100, the answer fits in a 32-bit integer
        """, "uniquePaths(m:int, n:int)->int",
      [(3, 7), (3, 2), (1, 1), (7, 3), (10, 10), (23, 12)],
      """
      class Solution:
          def uniquePaths(self, m, n):
              row = [1] * n
              for _ in range(m - 1):
                  for j in range(1, n):
                      row[j] += row[j - 1]
              return row[-1]
      """, hint="paths(r, c) = paths(r-1, c) + paths(r, c-1)."),
    F("Longest Common Subsequence", 1143, "Medium", """
        Return the length of the longest common subsequence of `text1` and `text2` (characters in the same relative order, not necessarily contiguous), or 0 if there is none.

        Constraints:
        - 1 <= text1.length, text2.length <= 1000
        """, "longestCommonSubsequence(text1:string, text2:string)->int",
      [("abcde", "ace"), ("abc", "abc"), ("abc", "def"), ("bl", "yby"), ("oxcpqrsvwf", "shmtulqrypy"), ("AGGTAB", "GXTXAYB")],
      """
      class Solution:
          def longestCommonSubsequence(self, text1, text2):
              dp = [[0] * (len(text2) + 1) for _ in range(len(text1) + 1)]
              for i in range(1, len(text1) + 1):
                  for j in range(1, len(text2) + 1):
                      dp[i][j] = dp[i - 1][j - 1] + 1 if text1[i - 1] == text2[j - 1] else max(dp[i - 1][j], dp[i][j - 1])
              return dp[-1][-1]
      """, hint="dp[i][j] = LCS of the first i and first j characters."),
    F("Best Time to Buy and Sell Stock with Cooldown", 309, "Medium", """
        `prices[i]` is the price on day `i`. You may buy and sell any number of times, but you cannot hold more than one share, and after selling you must wait one day before buying again. Return the maximum profit.

        Constraints:
        - 1 <= prices.length <= 5000
        """, "maxProfit(prices:int[])->int",
      [([1, 2, 3, 0, 2],), ([1],), ([2, 1],), ([1, 2, 4],), ([6, 1, 3, 2, 4, 7],), ([1, 4, 2],)],
      """
      class Solution:
          def maxProfit(self, prices):
              hold, sold, rest = -float('inf'), 0, 0
              for p in prices:
                  hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
              return max(sold, rest)
      """, hint="Three states per day: holding, just sold, resting."),
    F("Coin Change II", 518, "Medium", """
        Given `coins` (unlimited supply of each) and an `amount`, return the number of combinations that make up that amount (order does not matter). Return 0 if impossible.

        Constraints:
        - 1 <= coins.length <= 300, 0 <= amount <= 5000, answer fits in a 32-bit integer
        """, "change(amount:int, coins:int[])->int",
      [(5, [1, 2, 5]), (3, [2]), (10, [10]), (0, [1]), (500, [3, 5, 7, 8, 9, 10, 11]), (100, [1, 5, 10, 25])],
      """
      class Solution:
          def change(self, amount, coins):
              dp = [1] + [0] * amount
              for c in coins:
                  for a in range(c, amount + 1):
                      dp[a] += dp[a - c]
              return dp[amount]
      """, hint="Loop over coins on the outside so each combination is counted once."),
    F("Target Sum", 494, "Medium", """
        Put a `+` or `-` in front of every number in `nums` and return the number of different sign assignments whose total equals `target`.

        Constraints:
        - 1 <= nums.length <= 20, 0 <= nums[i] <= 1000
        """, "findTargetSumWays(nums:int[], target:int)->int",
      [([1, 1, 1, 1, 1], 3), ([1], 1), ([1], 2), ([0, 0, 0], 0), ([1, 2, 3, 4, 5], 3), ([100], -200)],
      """
      class Solution:
          def findTargetSumWays(self, nums, target):
              dp = {0: 1}
              for x in nums:
                  nd = defaultdict(int)
                  for s, c in dp.items():
                      nd[s + x] += c; nd[s - x] += c
                  dp = nd
              return dp.get(target, 0)
      """, hint="Keep a map from running sum to the number of ways to reach it."),
    F("Interleaving String", 97, "Medium", """
        Return `true` if `s3` can be formed by interleaving `s1` and `s2`: merging them while keeping the relative order of each string's characters.

        Constraints:
        - 0 <= s1.length, s2.length <= 100, 0 <= s3.length <= 200
        """, "isInterleave(s1:string, s2:string, s3:string)->bool",
      [("aabcc", "dbbca", "aadbbcbcac"), ("aabcc", "dbbca", "aadbbbaccc"), ("", "", ""), ("a", "", "a"), ("a", "b", "ba"), ("ab", "bc", "babc"), ("a", "b", "abc")],
      """
      class Solution:
          def isInterleave(self, s1, s2, s3):
              if len(s1) + len(s2) != len(s3):
                  return False
              dp = [[False] * (len(s2) + 1) for _ in range(len(s1) + 1)]
              dp[0][0] = True
              for i in range(len(s1) + 1):
                  for j in range(len(s2) + 1):
                      if i and dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]:
                          dp[i][j] = True
                      if j and dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]:
                          dp[i][j] = True
              return dp[-1][-1]
      """, hint="dp[i][j]: can the first i of s1 and first j of s2 build the first i+j of s3?"),
    F("Longest Increasing Path in a Matrix", 329, "Hard", """
        Return the length of the longest strictly increasing path in an integer matrix. From each cell you may move up, down, left or right (no diagonals, no wrapping).

        Constraints:
        - 1 <= m, n <= 200
        """, "longestIncreasingPath(matrix:int[][])->int",
      [([[9, 9, 4], [6, 6, 8], [2, 1, 1]],), ([[3, 4, 5], [3, 2, 6], [2, 2, 1]],), ([[1]],), ([[1, 2], [4, 3]],), ([[7, 8, 9], [9, 7, 6], [7, 2, 3]],)],
      """
      class Solution:
          def longestIncreasingPath(self, matrix):
              R, C = len(matrix), len(matrix[0]); memo = {}
              def go(r, c):
                  if (r, c) in memo:
                      return memo[(r, c)]
                  best = 1
                  for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                      a, b = r + dr, c + dc
                      if 0 <= a < R and 0 <= b < C and matrix[a][b] > matrix[r][c]:
                          best = max(best, 1 + go(a, b))
                  memo[(r, c)] = best
                  return best
              return max(go(r, c) for r in range(R) for c in range(C))
      """, hint="DFS with memoisation; strictly increasing means the graph has no cycles."),
    F("Distinct Subsequences", 115, "Hard", """
        Return the number of distinct subsequences of `s` that equal `t`.

        Constraints:
        - 1 <= s.length, t.length <= 1000, answer fits in a 32-bit integer
        """, "numDistinct(s:string, t:string)->int",
      [("rabbbit", "rabbit"), ("babgbag", "bag"), ("a", "a"), ("abc", "d"), ("aaa", "aa"), ("abcabcabc", "abc")],
      """
      class Solution:
          def numDistinct(self, s, t):
              dp = [1] + [0] * len(t)
              for ch in s:
                  for j in range(len(t), 0, -1):
                      if t[j - 1] == ch:
                          dp[j] += dp[j - 1]
              return dp[-1]
      """, hint="dp[j] = number of ways to build the first j characters of t from what you have scanned so far."),
    F("Edit Distance", 72, "Medium", """
        Return the minimum number of operations (insert, delete or replace a character) needed to turn `word1` into `word2`.

        Constraints:
        - 0 <= word1.length, word2.length <= 500
        """, "minDistance(word1:string, word2:string)->int",
      [("horse", "ros"), ("intention", "execution"), ("", "a"), ("a", ""), ("abc", "abc"), ("kitten", "sitting")],
      """
      class Solution:
          def minDistance(self, word1, word2):
              m, n = len(word1), len(word2); dp = list(range(n + 1))
              for i in range(1, m + 1):
                  prev, dp[0] = dp[0], i
                  for j in range(1, n + 1):
                      cur = dp[j]
                      dp[j] = prev if word1[i - 1] == word2[j - 1] else 1 + min(prev, dp[j], dp[j - 1])
                      prev = cur
              return dp[n]
      """, hint="dp[i][j] = cost to turn the first i characters of word1 into the first j of word2."),
    F("Burst Balloons", 312, "Hard", """
        You have balloons with numbers `nums[i]`. Bursting balloon `i` earns `nums[i-1] * nums[i] * nums[i+1]` coins (a missing neighbour counts as 1). Return the maximum coins you can collect by bursting all balloons in the best order.

        Constraints:
        - 1 <= nums.length <= 300, 0 <= nums[i] <= 100
        """, "maxCoins(nums:int[])->int",
      [([3, 1, 5, 8],), ([1, 5],), ([7],), ([2, 4, 6, 8, 3],), ([9, 76, 64, 21],), ([0, 5, 0],)],
      """
      class Solution:
          def maxCoins(self, nums):
              a = [1] + nums + [1]; n = len(a)
              dp = [[0] * n for _ in range(n)]
              for length in range(2, n):
                  for l in range(n - length):
                      r = l + length
                      dp[l][r] = max(dp[l][k] + dp[k][r] + a[l] * a[k] * a[r] for k in range(l + 1, r))
              return dp[0][n - 1]
      """, hint="Think of the LAST balloon burst in a range; it splits the problem into two independent halves."),
    F("Regular Expression Matching", 10, "Hard", """
        Implement matching of string `s` against pattern `p`, where `'.'` matches any single character and `'*'` matches zero or more of the preceding element. The match must cover the **entire** string.

        Constraints:
        - 1 <= s.length <= 20, 1 <= p.length <= 20 (the tests also use an empty `s`)
        - `*` is never the first character of `p` and always follows a letter or '.'
        """, "isMatch(s:string, p:string)->bool",
      [("aa", "a"), ("aa", "a*"), ("ab", ".*"), ("aab", "c*a*b"), ("mississippi", "mis*is*p*."), ("", "a*"), ("a", "ab*"), ("ab", ".*c")],
      """
      class Solution:
          def isMatch(self, s, p):
              @lru_cache(None)
              def go(i, j):
                  if j == len(p):
                      return i == len(s)
                  first = i < len(s) and p[j] in (s[i], '.')
                  if j + 1 < len(p) and p[j + 1] == '*':
                      return go(i, j + 2) or (first and go(i + 1, j))
                  return first and go(i + 1, j + 1)
              return go(0, 0)
      """, hint="dp over (i, j); on 'x*' either skip it entirely or consume one matching character and stay."),
]

G25 = [
    F("Insert Interval", 57, "Medium", """
        `intervals` is a list of non-overlapping intervals sorted by start. Insert `newInterval` and merge any overlaps so the result is still sorted and non-overlapping. Return the resulting list.

        Constraints:
        - 0 <= intervals.length <= 10^4
        """, "insert(intervals:int[][], newInterval:int[])->int[][]",
      [([[1, 3], [6, 9]], [2, 5]), ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]), ([], [5, 7]), ([[1, 5]], [2, 3]), ([[1, 5]], [6, 8]), ([[1, 5]], [0, 0])],
      """
      class Solution:
          def insert(self, intervals, newInterval):
              res = []; s, e = newInterval; i = 0
              while i < len(intervals) and intervals[i][1] < s:
                  res.append(intervals[i]); i += 1
              while i < len(intervals) and intervals[i][0] <= e:
                  s = min(s, intervals[i][0]); e = max(e, intervals[i][1]); i += 1
              res.append([s, e])
              res += intervals[i:]
              return res
      """, hint="Three phases: intervals before, intervals that overlap (merge them), intervals after."),
    F("Merge Intervals", 56, "Medium", """
        Merge all overlapping intervals and return the non-overlapping intervals that cover the same ranges. Intervals that touch (like `[1,4]` and `[4,5]`) overlap.

        Constraints:
        - 1 <= intervals.length <= 10^4
        """, "merge(intervals:int[][])->int[][]",
      [([[1, 3], [2, 6], [8, 10], [15, 18]],), ([[1, 4], [4, 5]],), ([[1, 4], [0, 4]],), ([[1, 4], [2, 3]],), ([[1, 4], [0, 0]],), ([[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]],)],
      """
      class Solution:
          def merge(self, intervals):
              res = []
              for s, e in sorted(intervals):
                  if res and s <= res[-1][1]:
                      res[-1][1] = max(res[-1][1], e)
                  else:
                      res.append([s, e])
              return res
      """, cmp="sorted", hint="Sort by start, then extend the last merged interval whenever the next one overlaps it."),
    F("Non-overlapping Intervals", 435, "Medium", """
        Return the minimum number of intervals to remove so that the rest are non-overlapping. Intervals that only touch at an endpoint do not overlap.

        Constraints:
        - 1 <= intervals.length <= 10^5
        """, "eraseOverlapIntervals(intervals:int[][])->int",
      [([[1, 2], [2, 3], [3, 4], [1, 3]],), ([[1, 2], [1, 2], [1, 2]],), ([[1, 2], [2, 3]],), ([[1, 100], [11, 22], [1, 11], [2, 12]],), ([[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]],)],
      """
      class Solution:
          def eraseOverlapIntervals(self, intervals):
              intervals.sort(key=lambda x: x[1]); end = -10**18; keep = 0
              for s, e in intervals:
                  if s >= end:
                      keep += 1; end = e
              return len(intervals) - keep
      """, hint="Greedy: always keep the interval that ends earliest."),
    F("Meeting Rooms", 252, "Easy", """
        `intervals[i] = [start, end]` are meeting times. Return `true` if one person could attend all meetings (no two overlap; meetings that end exactly when another starts are fine).

        Constraints:
        - 0 <= intervals.length <= 10^4
        """, "canAttendMeetings(intervals:int[][])->bool",
      [([[0, 30], [5, 10], [15, 20]],), ([[7, 10], [2, 4]],), ([],), ([[1, 5], [5, 8]],), ([[1, 5], [4, 8]],)],
      """
      class Solution:
          def canAttendMeetings(self, intervals):
              iv = sorted(intervals)
              return all(iv[i][1] <= iv[i + 1][0] for i in range(len(iv) - 1))
      """, hint="Sort by start time and compare neighbours."),
    F("Meeting Rooms II", 253, "Medium", """
        Return the minimum number of conference rooms needed to hold all meetings `intervals[i] = [start, end]`. A meeting may start in a room at the same moment another one ends there.

        Constraints:
        - 0 <= intervals.length <= 10^4
        """, "minMeetingRooms(intervals:int[][])->int",
      [([[0, 30], [5, 10], [15, 20]],), ([[7, 10], [2, 4]],), ([],), ([[1, 5], [5, 10]],), ([[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]],)],
      """
      class Solution:
          def minMeetingRooms(self, intervals):
              starts = sorted(i[0] for i in intervals); ends = sorted(i[1] for i in intervals)
              j = best = cur = 0
              for s in starts:
                  while ends[j] <= s:
                      j += 1; cur -= 1
                  cur += 1; best = max(best, cur)
              return best
      """, hint="Sweep over sorted starts and ends, or keep a min-heap of room end times."),
    F("Minimum Interval to Include Each Query", 1851, "Hard", """
        `intervals[i] = [left, right]` includes every integer in `left..right` (size `right - left + 1`). For each query value, return the size of the smallest interval containing it, or -1 if none does. Return the answers in the order of `queries`.

        Constraints:
        - 1 <= intervals.length, queries.length <= 10^5
        """, "minInterval(intervals:int[][], queries:int[])->int[]",
      [([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]), ([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]), ([[1, 1]], [1, 2]), ([[1, 5]], [3]), ([[5, 9], [1, 3], [2, 6]], [1, 4, 7, 10])],
      """
      class Solution:
          def minInterval(self, intervals, queries):
              iv = sorted(intervals); res = {}; h = []; i = 0
              for q in sorted(queries):
                  while i < len(iv) and iv[i][0] <= q:
                      l, r = iv[i]; heappush(h, (r - l + 1, r)); i += 1
                  while h and h[0][1] < q:
                      heappop(h)
                  res[q] = h[0][0] if h else -1
              return [res[q] for q in queries]
      """, hint="Process queries in sorted order, with a min-heap of (size, right) for intervals that already started."),
]

G26 = [
    F("Rotate Image", 48, "Medium", """
        Rotate an `n x n` matrix by 90 degrees clockwise, **in place**.

        Constraints:
        - 1 <= n <= 20
        """, "rotate(matrix:int[][])->void",
      [([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), ([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],), ([[1]],), ([[1, 2], [3, 4]],)],
      """
      class Solution:
          def rotate(self, matrix):
              n = len(matrix)
              for i in range(n):
                  for j in range(i + 1, n):
                      matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
              for row in matrix:
                  row.reverse()
      """, inplace="matrix", hint="Transpose, then reverse each row."),
    F("Spiral Matrix", 54, "Medium", """
        Return all elements of an `m x n` matrix in spiral order, starting at the top-left and going clockwise.

        Constraints:
        - 1 <= m, n <= 10
        """, "spiralOrder(matrix:int[][])->int[]",
      [([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],), ([[1]],), ([[1, 2], [3, 4], [5, 6]],), ([[1, 2, 3]],), ([[1], [2], [3]],)],
      """
      class Solution:
          def spiralOrder(self, matrix):
              res = []; t, b, l, r = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
              while t <= b and l <= r:
                  res += matrix[t][l:r + 1]; t += 1
                  res += [matrix[i][r] for i in range(t, b + 1)]; r -= 1
                  if t <= b:
                      res += matrix[b][l:r + 1][::-1]; b -= 1
                  if l <= r:
                      res += [matrix[i][l] for i in range(b, t - 1, -1)]; l += 1
              return res
      """, hint="Shrink four boundaries (top, bottom, left, right) as you walk each side."),
    F("Set Matrix Zeroes", 73, "Medium", """
        If a cell of an `m x n` matrix is 0, set its entire row and column to 0. Do it **in place**.

        Constraints:
        - 1 <= m, n <= 200
        """, "setZeroes(matrix:int[][])->void",
      [([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],), ([[1]],), ([[0]],), ([[1, 0]],), ([[1, 2, 3], [4, 5, 6]],)],
      """
      class Solution:
          def setZeroes(self, matrix):
              rows = {i for i, r in enumerate(matrix) if 0 in r}
              cols = {j for r in matrix for j, v in enumerate(r) if v == 0}
              for i in range(len(matrix)):
                  for j in range(len(matrix[0])):
                      if i in rows or j in cols:
                          matrix[i][j] = 0
      """, inplace="matrix", hint="Record which rows and columns contain a zero first, then zero them. O(1) space is possible by using the first row and column as markers."),
]

G27 = [
    R("Encode and Decode Strings", 271, "Medium", """
        Design an algorithm to encode a list of strings into a single string, and decode that string back to the original list. The strings may contain any characters, including the ones you might choose as separators.

        The tests call `decode(encode(strs))` and check that the same list comes back.

        Constraints:
        - 0 <= strs.length <= 200, 0 <= strs[i].length <= 200
        """, "Codec", "encode", "decode", "string[]",
      [["lint", "code", "love", "you"], ["we", "say", ":", "yes"], [""], [], ["a#b", "1#", "##"], ["hello world", "", "x"], ["4#abcd", "#", "12#"]],
      """
      class Codec:
          def encode(self, strs):
              return ''.join(str(len(s)) + '#' + s for s in strs)
          def decode(self, data):
              res = []; i = 0
              while i < len(data):
                  j = data.index('#', i); n = int(data[i:j])
                  res.append(data[j + 1:j + 1 + n]); i = j + 1 + n
              return res
      """, hint="Prefix every string with its length and a delimiter."),
    F("Plus One", 66, "Easy", """
        `digits` is a large non-negative integer stored as an array of its decimal digits, most significant digit first. Add one and return the resulting digit array.

        Constraints:
        - 1 <= digits.length <= 100, no leading zeros except the number 0
        """, "plusOne(digits:int[])->int[]",
      [([1, 2, 3],), ([4, 3, 2, 1],), ([9],), ([9, 9, 9],), ([0],), ([1, 9, 9],)],
      """
      class Solution:
          def plusOne(self, digits):
              for i in range(len(digits) - 1, -1, -1):
                  if digits[i] < 9:
                      digits[i] += 1
                      return digits
                  digits[i] = 0
              return [1] + digits
      """, hint="Carry from the right; if every digit was 9 you need a new leading 1."),
    F("Pow(x, n)", 50, "Medium", """
        Implement `pow(x, n)`: return `x` raised to the integer power `n`. `n` can be negative.

        Constraints:
        - -100.0 < x < 100.0, -2^31 <= n <= 2^31 - 1
        - the result fits in a double
        """, "myPow(x:double, n:int)->double",
      [(2.0, 10), (2.1, 3), (2.0, -2), (1.0, 2147483647), (0.5, 8), (-2.0, 3), (2.0, 0), (-1.0, 2147483647), (0.00001, 2147483647)],
      """
      class Solution:
          def myPow(self, x, n):
              if n < 0:
                  x, n = 1 / x, -n
              r = 1.0
              while n:
                  if n & 1:
                      r *= x
                  x *= x; n >>= 1
              return r
      """, cmp="float", hint="Square the base and halve the exponent (fast exponentiation)."),
    F("Multiply Strings", 43, "Medium", """
        Multiply two non-negative integers given as decimal strings and return the product as a string. Do not convert the whole inputs to integers directly.

        Constraints:
        - 1 <= num1.length, num2.length <= 200, digits only, no leading zeros except "0"
        """, "multiply(num1:string, num2:string)->string",
      [("2", "3"), ("123", "456"), ("0", "123"), ("999", "999"), ("9133", "0"), ("123456789", "987654321")],
      """
      class Solution:
          def multiply(self, num1, num2):
              if num1 == '0' or num2 == '0':
                  return '0'
              res = [0] * (len(num1) + len(num2))
              for i in range(len(num1) - 1, -1, -1):
                  for j in range(len(num2) - 1, -1, -1):
                      s = int(num1[i]) * int(num2[j]) + res[i + j + 1]
                      res[i + j + 1] = s % 10; res[i + j] += s // 10
              return ''.join(map(str, res)).lstrip('0')
      """, hint="Schoolbook multiplication: digit i times digit j lands at position i + j + 1."),
    F("Reverse Integer", 7, "Medium", """
        Reverse the digits of a signed 32-bit integer `x`. If the reversed value falls outside the 32-bit signed range `[-2^31, 2^31 - 1]`, return 0. Assume the environment cannot store larger integers.

        Constraints:
        - -2^31 <= x <= 2^31 - 1
        """, "reverse(x:int)->int",
      [(123,), (-123,), (120,), (0,), (1534236469,), (-2147483412,), (1463847412,)],
      """
      class Solution:
          def reverse(self, x):
              r = int(str(abs(x))[::-1]) * (1 if x >= 0 else -1)
              return r if -2**31 <= r <= 2**31 - 1 else 0
      """, hint="Pop the last digit with % 10, push it with * 10, and check for overflow before it happens."),
]

G28 = [
    F("Single Number", 136, "Easy", """
        Every element in `nums` appears twice except one, which appears once. Return that single element using linear time and constant extra space.

        Constraints:
        - 1 <= nums.length <= 3 * 10^4
        """, "singleNumber(nums:int[])->int",
      [([2, 2, 1],), ([4, 1, 2, 1, 2],), ([1],), ([-1, -1, -2],), ([7, 3, 5, 3, 5],)],
      """
      class Solution:
          def singleNumber(self, nums):
              r = 0
              for x in nums:
                  r ^= x
              return r
      """, hint="XOR cancels equal pairs."),
    F("Number of 1 Bits", 191, "Easy", """
        Return the number of `1` bits in the binary representation of the positive integer `n` (its Hamming weight).

        Constraints:
        - 1 <= n <= 2^31 - 1
        """, "hammingWeight(n:int)->int",
      [(11,), (128,), (2147483645,), (1,), (255,), (2147483647,)],
      """
      class Solution:
          def hammingWeight(self, n):
              return bin(n).count('1')
      """, hint="n & (n - 1) clears the lowest set bit."),
    F("Counting Bits", 338, "Easy", """
        Return an array `ans` of length `n + 1` where `ans[i]` is the number of `1` bits in the binary representation of `i`.

        Constraints:
        - 0 <= n <= 10^5
        """, "countBits(n:int)->int[]",
      [(2,), (5,), (0,), (16,), (33,)],
      """
      class Solution:
          def countBits(self, n):
              ans = [0] * (n + 1)
              for i in range(1, n + 1):
                  ans[i] = ans[i >> 1] + (i & 1)
              return ans
      """, hint="bits(i) = bits(i >> 1) + (i & 1)."),
    F("Reverse Bits", 190, "Easy", """
        Reverse the bits of a 32-bit **unsigned** integer `n` and return the result as an unsigned value (so the answer can be up to 4294967295).

        Constraints:
        - 0 <= n <= 2^32 - 1
        """, "reverseBits(n:long)->long",
      [(43261596,), (4294967293,), (0,), (1,), (4294967295,), (2,)],
      """
      class Solution:
          def reverseBits(self, n):
              r = 0
              for _ in range(32):
                  r = (r << 1) | (n & 1); n >>= 1
              return r
      """, hint="Shift the result left and copy the lowest bit of n, 32 times."),
    F("Missing Number", 268, "Easy", """
        `nums` contains `n` distinct numbers taken from the range `[0, n]`. Return the one number in that range that is missing.

        Constraints:
        - 1 <= n <= 10^4
        """, "missingNumber(nums:int[])->int",
      [([3, 0, 1],), ([0, 1],), ([9, 6, 4, 2, 3, 5, 7, 0, 1],), ([0],), ([1],)],
      """
      class Solution:
          def missingNumber(self, nums):
              n = len(nums)
              return n * (n + 1) // 2 - sum(nums)
      """, hint="Either the sum formula or XOR of all indices and values."),
    F("Sum of Two Integers", 371, "Medium", """
        Return the sum of two integers `a` and `b` **without using the operators `+` and `-`**.

        Constraints:
        - -1000 <= a, b <= 1000
        """, "getSum(a:int, b:int)->int",
      [(1, 2), (2, 3), (-1, 1), (-5, -7), (0, 0), (1000, -1000), (-2, 3)],
      """
      class Solution:
          def getSum(self, a, b):
              return a + b
      """, hint="XOR adds without carry; AND shifted left is the carry. Repeat until there is no carry."),
]
