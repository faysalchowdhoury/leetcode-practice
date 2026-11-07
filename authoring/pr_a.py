from dsl import F, D, R

V = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"]
def board(rows, edit=None):
    b = [list(r) for r in rows]
    if edit:
        for (r, c, v) in edit:
            b[r][c] = v
    return b

G01 = [
    F("Contains Duplicate", 217, "Easy", """
        Given an integer array `nums`, return `true` if any value appears at least twice, and `false` if every element is distinct.

        Constraints:
        - 1 <= nums.length <= 10^5
        - -10^9 <= nums[i] <= 10^9
        """, "containsDuplicate(nums:int[])->bool",
      [([1, 2, 3, 1],), ([1, 2, 3, 4],), ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],), ([0],), ([-1, -2, -3, -1],), (list(range(5000)) + [4999],), (list(range(5000)),)],
      """
      class Solution:
          def containsDuplicate(self, nums):
              return len(set(nums)) != len(nums)
      """, hint="A set remembers what you have already seen in O(1) per lookup."),
    F("Valid Anagram", 242, "Easy", """
        Given two strings `s` and `t`, return `true` if `t` is an anagram of `s` (same letters, same counts, any order), otherwise `false`.

        Constraints:
        - 1 <= s.length, t.length <= 5 * 10^4
        - `s` and `t` contain lowercase English letters
        """, "isAnagram(s:string, t:string)->bool",
      [("anagram", "nagaram"), ("rat", "car"), ("a", "a"), ("ab", "a"), ("aabb", "bbaa"), ("listen", "silent"), ("aacc", "ccac")],
      """
      class Solution:
          def isAnagram(self, s, t):
              return Counter(s) == Counter(t)
      """, hint="Count the letters of both strings and compare the counts."),
    F("Two Sum", 1, "Easy", """
        Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`.

        Exactly one solution exists, and you may not use the same element twice. The answer can be returned in any order.

        Constraints:
        - 2 <= nums.length <= 10^4
        - -10^9 <= nums[i], target <= 10^9
        """, "twoSum(nums:int[], target:int)->int[]",
      [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([3, 3], 6), ([-1, -2, -3, -4, -5], -8), ([0, 4, 3, 0], 0), ([1, 5, 9, 14], 23), (list(range(1, 3001)) + [10000, 10001], 20001)],
      """
      class Solution:
          def twoSum(self, nums, target):
              seen = {}
              for i, x in enumerate(nums):
                  if target - x in seen:
                      return [seen[target - x], i]
                  seen[x] = i
      """, cmp="sorted", hint="For each number, ask: have I already seen target - number?"),
    F("Group Anagrams", 49, "Medium", """
        Given an array of strings `strs`, group the anagrams together. The groups and the strings inside each group may be returned in any order.

        Constraints:
        - 1 <= strs.length <= 10^4
        - 0 <= strs[i].length <= 100, lowercase English letters
        """, "groupAnagrams(strs:string[])->string[][]",
      [(["eat", "tea", "tan", "ate", "nat", "bat"],), ([""],), (["a"],), (["abc", "bca", "cab", "xyz", "zyx"],), (["ab", "ba", "ab"],), (["", ""],)],
      """
      class Solution:
          def groupAnagrams(self, strs):
              d = defaultdict(list)
              for s in strs:
                  d[''.join(sorted(s))].append(s)
              return list(d.values())
      """, cmp="sorted_deep", hint="Anagrams share the same sorted letters (or the same letter-count signature). Use that as a dictionary key."),
    F("Valid Sudoku", 36, "Medium", """
        Determine whether a 9x9 Sudoku board is valid. Only the filled cells need to be checked:
        - each row has no repeated digit 1-9
        - each column has no repeated digit 1-9
        - each of the nine 3x3 boxes has no repeated digit 1-9

        Empty cells are `'.'`. A valid board is not necessarily solvable.
        """, "isValidSudoku(board:char[][])->bool",
      [(board(V),), (board(V, [(0, 0, '8')]),), (board(V, [(0, 2, '9')]),), (board(V, [(0, 1, '5')]),), (board(["........."] * 9),), (board(V, [(8, 8, '6')]),)],
      """
      class Solution:
          def isValidSudoku(self, board):
              rows, cols, boxes = defaultdict(set), defaultdict(set), defaultdict(set)
              for r in range(9):
                  for c in range(9):
                      v = board[r][c]
                      if v == '.':
                          continue
                      if v in rows[r] or v in cols[c] or v in boxes[(r // 3, c // 3)]:
                          return False
                      rows[r].add(v); cols[c].add(v); boxes[(r // 3, c // 3)].add(v)
              return True
      """, hint="Keep one set per row, per column and per 3x3 box. The box index is (row // 3, col // 3).", ex=1),
    F("Longest Consecutive Sequence", 128, "Medium", """
        Given an unsorted array of integers `nums`, return the length of the longest run of consecutive values (for example 4,5,6,7). Duplicates do not extend a run.

        Your algorithm should run in O(n) time.

        Constraints:
        - 0 <= nums.length <= 10^5
        - -10^9 <= nums[i] <= 10^9
        """, "longestConsecutive(nums:int[])->int",
      [([100, 4, 200, 1, 3, 2],), ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), ([],), ([1],), ([1, 2, 0, 1],), ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],), (list(range(0, 20000, 2)) + list(range(1, 100, 2)),)],
      """
      class Solution:
          def longestConsecutive(self, nums):
              s = set(nums); best = 0
              for x in s:
                  if x - 1 not in s:
                      y = x
                      while y + 1 in s:
                          y += 1
                      best = max(best, y - x + 1)
              return best
      """, hint="Only start counting from numbers that have no left neighbour (x - 1 is not in the set)."),
]

G02 = [
    F("Product of Array Except Self", 238, "Medium", """
        Given an integer array `nums`, return an array `answer` where `answer[i]` is the product of every element of `nums` except `nums[i]`.

        Do it in O(n) time without using division.

        Constraints:
        - 2 <= nums.length <= 10^5
        - -30 <= nums[i] <= 30, and every prefix/suffix product fits in a 32-bit integer
        """, "productExceptSelf(nums:int[])->int[]",
      [([1, 2, 3, 4],), ([-1, 1, 0, -3, 3],), ([2, 3],), ([0, 0],), ([1, 0],), ([5, -2, 4, 0, 1],), ([-1, -1, -1],)],
      """
      class Solution:
          def productExceptSelf(self, nums):
              n = len(nums); res = [1] * n
              p = 1
              for i in range(n):
                  res[i] = p; p *= nums[i]
              p = 1
              for i in range(n - 1, -1, -1):
                  res[i] *= p; p *= nums[i]
              return res
      """, hint="Answer[i] = (product of everything left of i) * (product of everything right of i). Two passes."),
    F("Best Time to Buy and Sell Stock", 121, "Easy", """
        `prices[i]` is the price of a stock on day `i`. Choose one day to buy and a later day to sell. Return the maximum profit, or 0 if no profit is possible.

        Constraints:
        - 1 <= prices.length <= 10^5
        - 0 <= prices[i] <= 10^4
        """, "maxProfit(prices:int[])->int",
      [([7, 1, 5, 3, 6, 4],), ([7, 6, 4, 3, 1],), ([1],), ([2, 4, 1],), ([3, 3, 5, 0, 0, 3, 1, 4],), ([1, 2],), ([2, 1, 2, 0, 1],)],
      """
      class Solution:
          def maxProfit(self, prices):
              lo = float('inf'); best = 0
              for p in prices:
                  lo = min(lo, p); best = max(best, p - lo)
              return best
      """, hint="Track the cheapest price seen so far while scanning once."),
    F("Maximum Subarray", 53, "Medium", """
        Given an integer array `nums`, find the contiguous non-empty subarray with the largest sum and return that sum.

        Constraints:
        - 1 <= nums.length <= 10^5
        - -10^4 <= nums[i] <= 10^4
        """, "maxSubArray(nums:int[])->int",
      [([-2, 1, -3, 4, -1, 2, 1, -5, 4],), ([1],), ([5, 4, -1, 7, 8],), ([-3, -2, -1],), ([-1, 0, -2],), ([2, -1, 2, -1, 2],)],
      """
      class Solution:
          def maxSubArray(self, nums):
              cur = best = nums[0]
              for x in nums[1:]:
                  cur = max(x, cur + x); best = max(best, cur)
              return best
      """, hint="Kadane: at each element decide whether to extend the previous subarray or start fresh."),
    F("Jump Game", 55, "Medium", """
        You start at index 0 of `nums`. Each `nums[i]` is the maximum jump length from index `i`. Return `true` if you can reach the last index, otherwise `false`.

        Constraints:
        - 1 <= nums.length <= 10^4
        - 0 <= nums[i] <= 10^5
        """, "canJump(nums:int[])->bool",
      [([2, 3, 1, 1, 4],), ([3, 2, 1, 0, 4],), ([0],), ([2, 0, 0],), ([1, 0, 1],), ([4, 0, 0, 0, 0, 1],), ([1, 1, 1, 1, 1],)],
      """
      class Solution:
          def canJump(self, nums):
              far = 0
              for i, x in enumerate(nums):
                  if i > far:
                      return False
                  far = max(far, i + x)
              return True
      """, hint="Track the farthest index reachable so far; if you ever stand beyond it, you are stuck."),
    F("Jump Game II", 45, "Medium", """
        Same setup as Jump Game, but the last index is always reachable. Return the minimum number of jumps needed to get from index 0 to the last index.

        Constraints:
        - 1 <= nums.length <= 10^4
        - 0 <= nums[i] <= 1000
        """, "jump(nums:int[])->int",
      [([2, 3, 1, 1, 4],), ([2, 3, 0, 1, 4],), ([1],), ([1, 2],), ([1, 1, 1, 1],), ([5, 9, 3, 2, 1, 0, 2, 3, 3, 1, 0, 0],), ([10, 1, 1, 1, 1, 1],)],
      """
      class Solution:
          def jump(self, nums):
              jumps = end = far = 0
              for i in range(len(nums) - 1):
                  far = max(far, i + nums[i])
                  if i == end:
                      jumps += 1; end = far
              return jumps
      """, hint="Think of it as BFS levels: every index reachable with k jumps forms one level."),
    F("Gas Station", 134, "Medium", """
        There are `n` stations on a circular route. Station `i` gives `gas[i]` fuel and driving from `i` to `i+1` costs `cost[i]`. You start with an empty tank.

        Return the index of the station you can start from to complete the full circle clockwise, or -1 if impossible. If a solution exists it is unique.

        Constraints:
        - n == gas.length == cost.length, 1 <= n <= 10^5
        - 0 <= gas[i], cost[i] <= 10^4
        """, "canCompleteCircuit(gas:int[], cost:int[])->int",
      [([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), ([2, 3, 4], [3, 4, 3]), ([5], [4]), ([5, 1, 2, 3, 4], [4, 4, 1, 5, 1]), ([3, 1, 1], [1, 2, 2]), ([2], [2]), ([4, 5, 2, 6, 5, 3], [3, 2, 7, 3, 2, 9])],
      """
      class Solution:
          def canCompleteCircuit(self, gas, cost):
              if sum(gas) < sum(cost):
                  return -1
              tank = start = 0
              for i in range(len(gas)):
                  tank += gas[i] - cost[i]
                  if tank < 0:
                      tank = 0; start = i + 1
              return start
      """, hint="If the total gas is at least the total cost an answer exists. Reset the start whenever the tank goes negative."),
    F("Hand of Straights", 846, "Medium", """
        Alice has cards with values `hand`. She wants to split them into groups of exactly `groupSize` consecutive values (for example 3,4,5). Return `true` if that is possible, otherwise `false`.

        Constraints:
        - 1 <= hand.length <= 10^4
        - 0 <= hand[i] <= 10^9, 1 <= groupSize <= hand.length
        """, "isNStraightHand(hand:int[], groupSize:int)->bool",
      [([1, 2, 3, 6, 2, 3, 4, 7, 8], 3), ([1, 2, 3, 4, 5], 4), ([1], 1), ([1, 1, 2, 2, 3, 3], 3), ([8, 10, 12], 3), ([5, 6, 7, 8, 9, 10], 2), ([1, 2, 3, 4], 1)],
      """
      class Solution:
          def isNStraightHand(self, hand, groupSize):
              if len(hand) % groupSize:
                  return False
              cnt = Counter(hand)
              for x in sorted(cnt):
                  c = cnt[x]
                  if c:
                      for y in range(x, x + groupSize):
                          if cnt[y] < c:
                              return False
                          cnt[y] -= c
              return True
      """, hint="Always start a group from the smallest remaining card."),
    F("Merge Triplets to Form Target Triplet", 1899, "Medium", """
        You are given `triplets`, where each is `[a, b, c]`, and a `target` triplet. In one operation pick two triplets and replace the second with `[max(a1,a2), max(b1,b2), max(c1,c2)]`.

        Return `true` if the target can become one of the triplets after any number of operations, otherwise `false`.

        Constraints:
        - 1 <= triplets.length <= 10^5
        - 1 <= values <= 1000
        """, "mergeTriplets(triplets:int[][], target:int[])->bool",
      [([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]), ([[3, 4, 5], [4, 5, 6]], [3, 2, 5]), ([[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], [5, 5, 5]), ([[1, 1, 1]], [1, 1, 1]), ([[1, 2, 3]], [1, 2, 4]), ([[1, 3, 4], [2, 5, 8]], [2, 5, 8])],
      """
      class Solution:
          def mergeTriplets(self, triplets, target):
              got = [False] * 3
              for t in triplets:
                  if t[0] <= target[0] and t[1] <= target[1] and t[2] <= target[2]:
                      for i in range(3):
                          if t[i] == target[i]:
                              got[i] = True
              return all(got)
      """, hint="Any triplet that exceeds the target in a position can never be used. Among the rest, check each target value can be matched."),
    F("Partition Labels", 763, "Medium", """
        Split string `s` into as many parts as possible so that each letter appears in at most one part. Return the sizes of the parts in order.

        Constraints:
        - 1 <= s.length <= 500, lowercase English letters
        """, "partitionLabels(s:string)->int[]",
      [("ababcbacadefegdehijhklij",), ("eccbbbbdec",), ("a",), ("abc",), ("caedbdedda",), ("aaabbb",)],
      """
      class Solution:
          def partitionLabels(self, s):
              last = {c: i for i, c in enumerate(s)}
              res = []; start = end = 0
              for i, c in enumerate(s):
                  end = max(end, last[c])
                  if i == end:
                      res.append(end - start + 1); start = i + 1
              return res
      """, hint="Record the last position of every letter, then extend the current part's end as you scan."),
    F("Valid Parenthesis String", 678, "Medium", """
        A string contains `'('`, `')'` and `'*'`. A `'*'` may be treated as `'('`, `')'` or an empty string. Return `true` if the string can be made a valid balanced parentheses string.

        Constraints:
        - 1 <= s.length <= 100
        """, "checkValidString(s:string)->bool",
      [("()",), ("(*)",), ("(*))",), ("(",), ("*",), (")(",), ("((*)",), ("**((*",), ("(((((*)))**",)],
      """
      class Solution:
          def checkValidString(self, s):
              lo = hi = 0
              for c in s:
                  if c == '(':
                      lo += 1; hi += 1
                  elif c == ')':
                      lo -= 1; hi -= 1
                  else:
                      lo -= 1; hi += 1
                  if hi < 0:
                      return False
                  lo = max(lo, 0)
              return lo == 0
      """, hint="Keep the range [lo, hi] of possible open-parenthesis counts."),
]

G03 = [
    F("Valid Palindrome", 125, "Easy", """
        A phrase is a palindrome if, after lowercasing it and removing every non-alphanumeric character, it reads the same forwards and backwards. Return `true` if `s` is a palindrome.

        Constraints:
        - 1 <= s.length <= 2 * 10^5, printable ASCII
        """, "isPalindrome(s:string)->bool",
      [("A man, a plan, a canal: Panama",), ("race a car",), (" ",), ("0P",), ("ab_a",), ("Was it a car or a cat I saw?",)],
      """
      class Solution:
          def isPalindrome(self, s):
              t = [c.lower() for c in s if c.isalnum()]
              return t == t[::-1]
      """, hint="Two pointers moving inward, skipping characters that are not letters or digits."),
    F("Two Sum II - Input Array Is Sorted", 167, "Medium", """
        `numbers` is sorted in non-decreasing order. Find the two numbers that add up to `target` and return their **1-based** indices `[index1, index2]` with `index1 < index2`.

        Exactly one solution exists. Use only constant extra space.

        Constraints:
        - 2 <= numbers.length <= 3 * 10^4
        - -1000 <= numbers[i], target <= 1000
        """, "twoSum(numbers:int[], target:int)->int[]",
      [([2, 7, 11, 15], 9), ([2, 3, 4], 6), ([-1, 0], -1), ([1, 2, 3, 4, 4, 9, 56, 90], 8), ([5, 25, 75], 100), ([-5, -3, 0, 3, 8], 0)],
      """
      class Solution:
          def twoSum(self, numbers, target):
              l, r = 0, len(numbers) - 1
              while l < r:
                  s = numbers[l] + numbers[r]
                  if s == target:
                      return [l + 1, r + 1]
                  if s < target:
                      l += 1
                  else:
                      r -= 1
      """, hint="Sorted input: move the left pointer up if the sum is too small, the right pointer down if too big."),
    F("3Sum", 15, "Medium", """
        Return all unique triplets `[nums[i], nums[j], nums[k]]` with distinct indices such that the three numbers sum to 0. The answer must not contain duplicate triplets, but may be in any order.

        Constraints:
        - 3 <= nums.length <= 3000
        - -10^5 <= nums[i] <= 10^5
        """, "threeSum(nums:int[])->int[][]",
      [([-1, 0, 1, 2, -1, -4],), ([0, 1, 1],), ([0, 0, 0],), ([0, 0, 0, 0],), ([-2, 0, 1, 1, 2],), ([3, 0, -2, -1, 1, 2],), ([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],)],
      """
      class Solution:
          def threeSum(self, nums):
              nums.sort(); res = []
              for i in range(len(nums) - 2):
                  if i and nums[i] == nums[i - 1]:
                      continue
                  l, r = i + 1, len(nums) - 1
                  while l < r:
                      s = nums[i] + nums[l] + nums[r]
                      if s < 0:
                          l += 1
                      elif s > 0:
                          r -= 1
                      else:
                          res.append([nums[i], nums[l], nums[r]])
                          l += 1
                          while l < r and nums[l] == nums[l - 1]:
                              l += 1
              return res
      """, cmp="sorted_deep", hint="Sort, fix one number, then run Two Sum II on the rest. Skip equal neighbours to avoid duplicates."),
    F("Container With Most Water", 11, "Medium", """
        `height[i]` is the height of a vertical line at position `i`. Pick two lines that together with the x-axis form a container holding the most water, and return that amount.

        Constraints:
        - 2 <= height.length <= 10^5
        - 0 <= height[i] <= 10^4
        """, "maxArea(height:int[])->int",
      [([1, 8, 6, 2, 5, 4, 8, 3, 7],), ([1, 1],), ([4, 3, 2, 1, 4],), ([1, 2, 1],), ([2, 3, 4, 5, 18, 17, 6],), ([0, 0],)],
      """
      class Solution:
          def maxArea(self, height):
              l, r = 0, len(height) - 1; best = 0
              while l < r:
                  best = max(best, (r - l) * min(height[l], height[r]))
                  if height[l] < height[r]:
                      l += 1
                  else:
                      r -= 1
              return best
      """, hint="Start with the widest container; moving the shorter wall is the only move that can help."),
    F("Trapping Rain Water", 42, "Hard", """
        Given `n` non-negative integers representing an elevation map where each bar has width 1, compute how much water it can trap after raining.

        Constraints:
        - 1 <= height.length <= 2 * 10^4
        - 0 <= height[i] <= 10^5
        """, "trap(height:int[])->int",
      [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), ([4, 2, 0, 3, 2, 5],), ([1],), ([3, 0, 3],), ([5, 4, 1, 2],), ([2, 0, 2],)],
      """
      class Solution:
          def trap(self, height):
              l, r = 0, len(height) - 1; lm = rm = water = 0
              while l < r:
                  if height[l] < height[r]:
                      lm = max(lm, height[l]); water += lm - height[l]; l += 1
                  else:
                      rm = max(rm, height[r]); water += rm - height[r]; r -= 1
              return water
      """, hint="Water above a bar = min(tallest left, tallest right) - bar. Two pointers can track both maxima."),
]

G04 = [
    F("Longest Substring Without Repeating Characters", 3, "Medium", """
        Return the length of the longest substring of `s` that contains no repeated character.

        Constraints:
        - 0 <= s.length <= 5 * 10^4
        """, "lengthOfLongestSubstring(s:string)->int",
      [("abcabcbb",), ("bbbbb",), ("pwwkew",), ("",), (" ",), ("dvdf",), ("abba",), ("tmmzuxt",)],
      """
      class Solution:
          def lengthOfLongestSubstring(self, s):
              last = {}; l = best = 0
              for r, c in enumerate(s):
                  if c in last and last[c] >= l:
                      l = last[c] + 1
                  last[c] = r; best = max(best, r - l + 1)
              return best
      """, hint="Slide a window; when a repeat enters, move the left edge just past its previous occurrence."),
    F("Longest Repeating Character Replacement", 424, "Medium", """
        You may change at most `k` characters of the uppercase string `s` to any other uppercase letter. Return the length of the longest substring that can be made of a single repeated letter.

        Constraints:
        - 1 <= s.length <= 10^5
        - 0 <= k <= s.length
        """, "characterReplacement(s:string, k:int)->int",
      [("ABAB", 2), ("AABABBA", 1), ("A", 0), ("AAAA", 2), ("ABCDE", 1), ("ABBB", 2), ("BAAAB", 2)],
      """
      class Solution:
          def characterReplacement(self, s, k):
              cnt = Counter(); l = best = mx = 0
              for r, c in enumerate(s):
                  cnt[c] += 1; mx = max(mx, cnt[c])
                  while (r - l + 1) - mx > k:
                      cnt[s[l]] -= 1; l += 1
                  best = max(best, r - l + 1)
              return best
      """, hint="A window is valid when (window size - count of its most common letter) <= k."),
    F("Permutation in String", 567, "Medium", """
        Given strings `s1` and `s2`, return `true` if some permutation of `s1` appears as a contiguous substring of `s2`.

        Constraints:
        - 1 <= s1.length, s2.length <= 10^4, lowercase English letters
        """, "checkInclusion(s1:string, s2:string)->bool",
      [("ab", "eidbaooo"), ("ab", "eidboaoo"), ("a", "a"), ("abc", "ab"), ("adc", "dcda"), ("hello", "ooolleoooleh")],
      """
      class Solution:
          def checkInclusion(self, s1, s2):
              n = len(s1)
              if n > len(s2):
                  return False
              need = Counter(s1); win = Counter(s2[:n])
              if need == win:
                  return True
              for i in range(n, len(s2)):
                  win[s2[i]] += 1; win[s2[i - n]] -= 1
                  if win[s2[i - n]] == 0:
                      del win[s2[i - n]]
                  if need == win:
                      return True
              return False
      """, hint="Slide a fixed-size window of length len(s1) and compare letter counts."),
    F("Minimum Window Substring", 76, "Hard", """
        Given strings `s` and `t`, return the shortest substring of `s` that contains every character of `t` (including duplicates). Return `""` if no such substring exists.

        The tests only use inputs where the answer is unique.

        Constraints:
        - 1 <= s.length, t.length <= 10^5
        """, "minWindow(s:string, t:string)->string",
      [("ADOBECODEBANC", "ABC"), ("a", "a"), ("a", "aa"), ("ab", "b"), ("aa", "aa"), ("cabwefgewcwaefgcf", "cae"), ("bba", "ab")],
      """
      class Solution:
          def minWindow(self, s, t):
              need = Counter(t); missing = len(t); l = 0; best = (float('inf'), 0, 0)
              for r, c in enumerate(s):
                  if need[c] > 0:
                      missing -= 1
                  need[c] -= 1
                  while missing == 0:
                      if r - l + 1 < best[0]:
                          best = (r - l + 1, l, r)
                      need[s[l]] += 1
                      if need[s[l]] > 0:
                          missing += 1
                      l += 1
              return '' if best[0] == float('inf') else s[best[1]:best[2] + 1]
      """, hint="Expand right until the window covers t, then shrink from the left while it still does."),
]
