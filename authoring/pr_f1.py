from dsl import F, D, R

# LeetCode-only problems, part 1: arrays, strings, searching, linked lists, design.

L_HASH = [
    F("Contains Duplicate II", 219, "Easy", """
        Return `true` if there are two distinct indices `i` and `j` with `nums[i] == nums[j]` and `|i - j| <= k`.

        Constraints:
        - 1 <= nums.length <= 10^5, 0 <= k <= 10^5
        """, "containsNearbyDuplicate(nums:int[], k:int)->bool",
      [([1, 2, 3, 1], 3), ([1, 0, 1, 1], 1), ([1, 2, 3, 1, 2, 3], 2), ([1], 1), ([99, 99], 2), ([1, 2, 1], 1)],
      """
      class Solution:
          def containsNearbyDuplicate(self, nums, k):
              last = {}
              for i, x in enumerate(nums):
                  if x in last and i - last[x] <= k:
                      return True
                  last[x] = i
              return False
      """, hint="Remember the last index of each value."),
    F("Ransom Note", 383, "Easy", """
        Return `true` if `ransomNote` can be built from the letters of `magazine`, using each magazine letter at most once.

        Constraints:
        - 1 <= ransomNote.length, magazine.length <= 10^5, lowercase letters
        """, "canConstruct(ransomNote:string, magazine:string)->bool",
      [("a", "b"), ("aa", "ab"), ("aa", "aab"), ("abc", "cba"), ("aab", "baa"), ("zz", "z")],
      """
      class Solution:
          def canConstruct(self, ransomNote, magazine):
              return not (Counter(ransomNote) - Counter(magazine))
      """, hint="Count the letters of the magazine and spend them."),
    F("Isomorphic Strings", 205, "Easy", """
        Two strings are isomorphic if the characters of `s` can be replaced to get `t`, with every occurrence of a character replaced by the same character and no two different characters mapping to the same one. Return `true` if `s` and `t` are isomorphic.

        Constraints:
        - 1 <= s.length <= 5 * 10^4, t.length == s.length
        """, "isIsomorphic(s:string, t:string)->bool",
      [("egg", "add"), ("foo", "bar"), ("paper", "title"), ("badc", "baba"), ("ab", "aa"), ("a", "a")],
      """
      class Solution:
          def isIsomorphic(self, s, t):
              return len(set(s)) == len(set(t)) == len(set(zip(s, t)))
      """, hint="The mapping must be one-to-one in both directions."),
    F("Word Pattern", 290, "Easy", """
        Given a `pattern` of letters and a string `s` of space-separated words, return `true` if `s` follows the pattern: there is a one-to-one mapping between pattern letters and words.

        Constraints:
        - 1 <= pattern.length <= 300, 1 <= s.length <= 3000
        """, "wordPattern(pattern:string, s:string)->bool",
      [("abba", "dog cat cat dog"), ("abba", "dog cat cat fish"), ("aaaa", "dog cat cat dog"), ("abba", "dog dog dog dog"), ("abc", "b c a"), ("a", "a")],
      """
      class Solution:
          def wordPattern(self, pattern, s):
              w = s.split()
              return len(w) == len(pattern) and len(set(pattern)) == len(set(w)) == len(set(zip(pattern, w)))
      """, hint="Same idea as Isomorphic Strings, on words."),
]

L_GREEDY = [
    F("Best Time to Buy and Sell Stock II", 122, "Medium", """
        `prices[i]` is the price on day `i`. You may buy and sell as many times as you like, but hold at most one share at a time. Return the maximum profit.

        Constraints:
        - 1 <= prices.length <= 3 * 10^4
        """, "maxProfit(prices:int[])->int",
      [([7, 1, 5, 3, 6, 4],), ([1, 2, 3, 4, 5],), ([7, 6, 4, 3, 1],), ([1],), ([2, 1, 2, 0, 1],), ([3, 3, 5, 0, 0, 3, 1, 4],)],
      """
      class Solution:
          def maxProfit(self, prices):
              return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))
      """, hint="Collect every upward step."),
    F("Maximum Sum Circular Subarray", 918, "Medium", """
        `nums` is a circular array (the end connects to the start). Return the maximum possible sum of a non-empty subarray, where the subarray may wrap around the end.

        Constraints:
        - 1 <= nums.length <= 3 * 10^4
        """, "maxSubarraySumCircular(nums:int[])->int",
      [([1, -2, 3, -2],), ([5, -3, 5],), ([-3, -2, -3],), ([3, -1, 2, -1],), ([2, -2, 2, 7, 8, 0],), ([1],)],
      """
      class Solution:
          def maxSubarraySumCircular(self, nums):
              total = cur_max = cur_min = 0; best = nums[0]; worst = nums[0]
              for x in nums:
                  cur_max = max(cur_max + x, x); best = max(best, cur_max)
                  cur_min = min(cur_min + x, x); worst = min(worst, cur_min)
                  total += x
              return best if best < 0 else max(best, total - worst)
      """, hint="Either the best subarray is normal (Kadane), or it wraps: total minus the worst subarray."),
    F("Majority Element", 169, "Easy", """
        Return the element that appears more than `n / 2` times in `nums`. The majority element always exists.

        Constraints:
        - 1 <= nums.length <= 5 * 10^4
        """, "majorityElement(nums:int[])->int",
      [([3, 2, 3],), ([2, 2, 1, 1, 1, 2, 2],), ([1],), ([6, 5, 5],), ([1, 1, 2, 2, 2],), ([-1, -1, -1, 3, 4],)],
      """
      class Solution:
          def majorityElement(self, nums):
              c = None; n = 0
              for x in nums:
                  if n == 0:
                      c = x
                  n += 1 if x == c else -1
              return c
      """, hint="Boyer-Moore voting: O(1) space."),
    F("H-Index", 274, "Medium", """
        `citations[i]` is the number of citations of paper `i`. Return the researcher's h-index: the largest `h` such that at least `h` papers have at least `h` citations each.

        Constraints:
        - 1 <= citations.length <= 5000
        """, "hIndex(citations:int[])->int",
      [([3, 0, 6, 1, 5],), ([1, 3, 1],), ([0],), ([100],), ([4, 4, 4, 4],), ([0, 0, 0],)],
      """
      class Solution:
          def hIndex(self, citations):
              c = sorted(citations, reverse=True); h = 0
              for i, x in enumerate(c):
                  if x >= i + 1:
                      h = i + 1
              return h
      """, hint="Sort descending; the h-index is the last position i where citations[i] >= i + 1."),
    F("Candy", 135, "Hard", """
        Children stand in a line with ratings `ratings[i]`. Give each child at least one candy, and any child with a higher rating than an adjacent neighbour must get more candy than that neighbour. Return the minimum total candies.

        Constraints:
        - 1 <= ratings.length <= 2 * 10^4
        """, "candy(ratings:int[])->int",
      [([1, 0, 2],), ([1, 2, 2],), ([1],), ([1, 3, 2, 2, 1],), ([1, 2, 87, 87, 87, 2, 1],), ([5, 4, 3, 2, 1],)],
      """
      class Solution:
          def candy(self, ratings):
              n = len(ratings); c = [1] * n
              for i in range(1, n):
                  if ratings[i] > ratings[i - 1]:
                      c[i] = c[i - 1] + 1
              for i in range(n - 2, -1, -1):
                  if ratings[i] > ratings[i + 1]:
                      c[i] = max(c[i], c[i + 1] + 1)
              return sum(c)
      """, hint="Two passes: left-to-right for the left neighbour, right-to-left for the right neighbour."),
]

L_INPLACE = [
    F("Merge Sorted Array", 88, "Easy", """
        `nums1` has length `m + n`: its first `m` values are sorted data and the last `n` are zeros reserved for the merge. `nums2` has `n` sorted values. Merge `nums2` into `nums1` **in place** so `nums1` is sorted.

        Constraints:
        - 0 <= m, n <= 200, 1 <= m + n <= 200
        """, "merge(nums1:int[], m:int, nums2:int[], n:int)->void",
      [([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3), ([1], 1, [], 0), ([0], 0, [1], 1), ([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3), ([2, 0], 1, [1], 1), ([1, 2, 4, 5, 6, 0], 5, [3], 1)],
      """
      class Solution:
          def merge(self, nums1, m, nums2, n):
              i, j, k = m - 1, n - 1, m + n - 1
              while j >= 0:
                  if i >= 0 and nums1[i] > nums2[j]:
                      nums1[k] = nums1[i]; i -= 1
                  else:
                      nums1[k] = nums2[j]; j -= 1
                  k -= 1
      """, inplace="nums1", hint="Fill from the back so you never overwrite unread values."),
    F("Remove Element", 27, "Easy", """
        Remove all occurrences of `val` from `nums` **in place** and return `k`, the number of remaining elements. The first `k` elements of `nums` must hold the elements that are not `val` (in any order). What is beyond `k` does not matter.

        Constraints:
        - 0 <= nums.length <= 100
        """, "removeElement(nums:int[], val:int)->int",
      [([3, 2, 2, 3], 3), ([0, 1, 2, 2, 3, 0, 4, 2], 2), ([], 0), ([1], 1), ([1], 2), ([4, 4, 4], 4), ([2, 3, 4], 5)],
      """
      class Solution:
          def removeElement(self, nums, val):
              k = 0
              for x in nums:
                  if x != val:
                      nums[k] = x; k += 1
              return k
      """, post="prefix_sorted", hint="Copy the elements you keep towards the front with a write pointer."),
    F("Remove Duplicates from Sorted Array", 26, "Easy", """
        `nums` is sorted in non-decreasing order. Remove duplicates **in place** so each value appears once, keeping the original relative order, and return `k`, the number of unique values. The first `k` elements of `nums` must be those values.

        Constraints:
        - 1 <= nums.length <= 3 * 10^4
        """, "removeDuplicates(nums:int[])->int",
      [([1, 1, 2],), ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4],), ([1],), ([1, 2, 3],), ([5, 5, 5, 5],)],
      """
      class Solution:
          def removeDuplicates(self, nums):
              k = 1
              for i in range(1, len(nums)):
                  if nums[i] != nums[k - 1]:
                      nums[k] = nums[i]; k += 1
              return k
      """, post="prefix", hint="Write a value only when it differs from the last written one."),
    F("Remove Duplicates from Sorted Array II", 80, "Medium", """
        `nums` is sorted. Remove duplicates **in place** so each value appears at most twice, keep the order, and return `k`, the new length. The first `k` elements must hold the result.

        Constraints:
        - 1 <= nums.length <= 3 * 10^4
        """, "removeDuplicates(nums:int[])->int",
      [([1, 1, 1, 2, 2, 3],), ([0, 0, 1, 1, 1, 1, 2, 3, 3],), ([1, 1, 1],), ([1],), ([1, 2, 2, 2, 3, 3, 3, 3],)],
      """
      class Solution:
          def removeDuplicates(self, nums):
              k = 0
              for x in nums:
                  if k < 2 or x != nums[k - 2]:
                      nums[k] = x; k += 1
              return k
      """, post="prefix", hint="Compare with the element two places behind the write position."),
    F("Rotate Array", 189, "Medium", """
        Rotate `nums` to the right by `k` steps, **in place**.

        Constraints:
        - 1 <= nums.length <= 10^5, 0 <= k <= 10^5
        """, "rotate(nums:int[], k:int)->void",
      [([1, 2, 3, 4, 5, 6, 7], 3), ([-1, -100, 3, 99], 2), ([1], 0), ([1, 2], 3), ([1, 2, 3], 3), ([1, 2, 3, 4, 5], 7)],
      """
      class Solution:
          def rotate(self, nums, k):
              n = len(nums); k %= n
              nums[:] = nums[n - k:] + nums[:n - k]
      """, inplace="nums", hint="Reverse the whole array, then reverse the first k and the rest separately."),
]

L_TWOPTR = [
    F("Is Subsequence", 392, "Easy", """
        Return `true` if `s` is a subsequence of `t` (it can be obtained by deleting some characters of `t` without reordering the rest).

        Constraints:
        - 0 <= s.length <= 100, 0 <= t.length <= 10^4
        """, "isSubsequence(s:string, t:string)->bool",
      [("abc", "ahbgdc"), ("axc", "ahbgdc"), ("", "ahbgdc"), ("a", ""), ("abc", "abc"), ("aaa", "aa")],
      """
      class Solution:
          def isSubsequence(self, s, t):
              i = 0
              for c in t:
                  if i < len(s) and s[i] == c:
                      i += 1
              return i == len(s)
      """, hint="Walk t once, advancing a pointer in s on every match."),
]

L_WINDOW = [
    F("Minimum Size Subarray Sum", 209, "Medium", """
        Return the minimal length of a contiguous subarray of positive integers whose sum is at least `target`, or 0 if none exists.

        Constraints:
        - 1 <= target <= 10^9, 1 <= nums.length <= 10^5, 1 <= nums[i] <= 10^4
        """, "minSubArrayLen(target:int, nums:int[])->int",
      [(7, [2, 3, 1, 2, 4, 3]), (4, [1, 4, 4]), (11, [1, 1, 1, 1, 1, 1, 1, 1]), (15, [1, 2, 3, 4, 5]), (100, [50, 50]), (3, [1, 1])],
      """
      class Solution:
          def minSubArrayLen(self, target, nums):
              l = s = 0; best = float('inf')
              for r, x in enumerate(nums):
                  s += x
                  while s >= target:
                      best = min(best, r - l + 1); s -= nums[l]; l += 1
              return 0 if best == float('inf') else best
      """, hint="Grow the window on the right, shrink on the left while the sum is still enough."),
    F("Substring with Concatenation of All Words", 30, "Hard", """
        `words` are strings of the same length. A concatenated substring is a substring of `s` that is exactly the concatenation of all words in some order. Return the starting indices of all such substrings in `s`, in any order.

        Constraints:
        - 1 <= s.length <= 10^4, 1 <= words.length <= 5000, 1 <= words[i].length <= 30
        """, "findSubstring(s:string, words:string[])->int[]",
      [("barfoothefoobarman", ["foo", "bar"]), ("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]), ("barfoofoobarthefoobarman", ["bar", "foo", "the"]), ("aaaaaa", ["aa", "aa"]), ("a", ["a"]), ("lingmindraboofooowingdingbarrwingmonkeypoundcake", ["fooo", "barr", "wing", "ding", "wing"])],
      """
      class Solution:
          def findSubstring(self, s, words):
              w = len(words[0]); n = len(words); need = Counter(words); res = []
              for i in range(len(s) - w * n + 1):
                  seen = Counter(); ok = True
                  for j in range(n):
                      word = s[i + j * w:i + (j + 1) * w]
                      seen[word] += 1
                      if seen[word] > need.get(word, 0):
                          ok = False; break
                  if ok:
                      res.append(i)
              return res
      """, cmp="sorted", hint="Check every start offset; a sliding window per word-length offset makes it faster."),
]

L_STRINGS = [
    F("Roman to Integer", 13, "Easy", """
        Convert a Roman numeral to an integer. Symbols: I=1, V=5, X=10, L=50, C=100, D=500, M=1000. A smaller symbol before a larger one is subtracted (IV = 4, IX = 9, XL, XC, CD, CM).

        Constraints:
        - 1 <= s.length <= 15, valid numeral in the range 1..3999
        """, "romanToInt(s:string)->int",
      [("III",), ("LVIII",), ("MCMXCIV",), ("IV",), ("IX",), ("MMMCMXCIX",)],
      """
      class Solution:
          def romanToInt(self, s):
              v = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}; t = 0
              for i, c in enumerate(s):
                  t += -v[c] if i + 1 < len(s) and v[c] < v[s[i + 1]] else v[c]
              return t
      """, hint="Subtract a symbol when the next one is larger."),
    F("Integer to Roman", 12, "Medium", """
        Convert an integer to a Roman numeral using the standard subtractive forms (IV, IX, XL, XC, CD, CM).

        Constraints:
        - 1 <= num <= 3999
        """, "intToRoman(num:int)->string",
      [(3,), (58,), (1994,), (4,), (3999,), (944,)],
      """
      class Solution:
          def intToRoman(self, num):
              vals = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
              out = ''
              for v, r in vals:
                  while num >= v:
                      out += r; num -= v
              return out
      """, hint="Greedily subtract the largest value from a table that includes the subtractive pairs."),
    F("Length of Last Word", 58, "Easy", """
        Return the length of the last word in `s`. A word is a maximal run of non-space characters.

        Constraints:
        - 1 <= s.length <= 10^4, `s` contains at least one word
        """, "lengthOfLastWord(s:string)->int",
      [("Hello World",), ("   fly me   to   the moon  ",), ("luffy is still joyboy",), ("a",), ("a ",)],
      """
      class Solution:
          def lengthOfLastWord(self, s):
              return len(s.split()[-1])
      """, hint="Scan from the end: skip spaces, then count letters."),
    F("Longest Common Prefix", 14, "Easy", """
        Return the longest common prefix of the strings in `strs`, or an empty string if there is none.

        Constraints:
        - 1 <= strs.length <= 200, 0 <= strs[i].length <= 200
        """, "longestCommonPrefix(strs:string[])->string",
      [(["flower", "flow", "flight"],), (["dog", "racecar", "car"],), (["a"],), (["", ""],), (["ab", "a"],), (["cir", "car"],)],
      """
      class Solution:
          def longestCommonPrefix(self, strs):
              p = strs[0]
              for s in strs[1:]:
                  while not s.startswith(p):
                      p = p[:-1]
              return p
      """, hint="Shrink the candidate prefix until every string starts with it."),
    F("Reverse Words in a String", 151, "Medium", """
        Reverse the order of the words in `s`. Words are separated by one or more spaces. The result must have words separated by a single space and no leading or trailing spaces.

        Constraints:
        - 1 <= s.length <= 10^4, at least one word
        """, "reverseWords(s:string)->string",
      [("the sky is blue",), ("  hello world  ",), ("a good   example",), ("a",), (" a b ",)],
      """
      class Solution:
          def reverseWords(self, s):
              return ' '.join(s.split()[::-1])
      """, hint="Split on whitespace, reverse, join."),
    F("Zigzag Conversion", 6, "Medium", """
        Write `s` in a zigzag pattern on `numRows` rows (down the rows, then diagonally up, and so on), then read it row by row. Return the resulting string.

        Constraints:
        - 1 <= s.length <= 1000, 1 <= numRows <= 1000
        """, "convert(s:string, numRows:int)->string",
      [("PAYPALISHIRING", 3), ("PAYPALISHIRING", 4), ("A", 1), ("AB", 1), ("ABCDE", 2), ("ABC", 5)],
      """
      class Solution:
          def convert(self, s, numRows):
              if numRows == 1 or numRows >= len(s):
                  return s
              rows = [''] * numRows; r = 0; d = 1
              for c in s:
                  rows[r] += c
                  if r == 0: d = 1
                  elif r == numRows - 1: d = -1
                  r += d
              return ''.join(rows)
      """, hint="Walk down and up the rows, appending each character to its row."),
    F("Find the Index of the First Occurrence in a String", 28, "Easy", """
        Return the index of the first occurrence of `needle` in `haystack`, or -1 if it does not occur.

        Constraints:
        - 1 <= haystack.length, needle.length <= 10^4
        """, "strStr(haystack:string, needle:string)->int",
      [("sadbutsad", "sad"), ("leetcode", "leeto"), ("a", "a"), ("mississippi", "issip"), ("abc", "c"), ("aaa", "aaaa")],
      """
      class Solution:
          def strStr(self, haystack, needle):
              return haystack.find(needle)
      """, hint="Try every start position (or implement KMP)."),
    F("Text Justification", 68, "Hard", """
        Format `words` into lines of exactly `maxWidth` characters, fully justified. Pack as many words as fit on each line, distributing extra spaces as evenly as possible between words (extra spaces go to the left gaps first). The last line, and any line with a single word, is left-justified and padded with spaces on the right.

        Constraints:
        - 1 <= words.length <= 300, 1 <= words[i].length <= maxWidth <= 100
        """, "fullJustify(words:string[], maxWidth:int)->string[]",
      [(["This", "is", "an", "example", "of", "text", "justification."], 16), (["What", "must", "be", "acknowledgment", "shall", "be"], 16), (["Science", "is", "what", "we", "understand", "well", "enough", "to", "explain", "to", "a", "computer.", "Art", "is", "everything", "else", "we", "do"], 20), (["a"], 1), (["a", "b", "c"], 1), (["Listen", "to", "many,", "speak", "to", "a", "few."], 6)],
      """
      class Solution:
          def fullJustify(self, words, maxWidth):
              res = []; i = 0
              while i < len(words):
                  j = i; length = 0
                  while j < len(words) and length + len(words[j]) + (j - i) <= maxWidth:
                      length += len(words[j]); j += 1
                  gaps = j - i - 1
                  if j == len(words) or gaps == 0:
                      line = ' '.join(words[i:j]); line += ' ' * (maxWidth - len(line))
                  else:
                      spaces = maxWidth - length; q, r = divmod(spaces, gaps); line = ''
                      for k in range(i, j - 1):
                          line += words[k] + ' ' * (q + (1 if k - i < r else 0))
                      line += words[j - 1]
                  res.append(line); i = j
              return res
      """, hint="Greedy line packing, then compute the gap sizes with divmod."),
]

L_STACK = [
    F("Simplify Path", 71, "Medium", """
        Convert an absolute Unix-style file path to its canonical form: it starts with `/`, directories are separated by one `/`, no trailing `/`, and `.` (current) and `..` (parent) are resolved. Three or more dots, like `...`, are ordinary names.

        Constraints:
        - 1 <= path.length <= 3000
        """, "simplifyPath(path:string)->string",
      [("/home/",), ("/home//foo/",), ("/home/user/Documents/../Pictures",), ("/../",), ("/.../a/../b/c/../d/./",), ("/a/./b/../../c/",)],
      """
      class Solution:
          def simplifyPath(self, path):
              st = []
              for p in path.split('/'):
                  if p == '..':
                      if st: st.pop()
                  elif p and p != '.':
                      st.append(p)
              return '/' + '/'.join(st)
      """, hint="Split on '/', and use a stack: '..' pops, names push."),
    F("Basic Calculator", 224, "Hard", """
        Evaluate an expression string containing non-negative integers, `+`, `-`, parentheses and spaces. A `-` may also be a unary minus (for example `-(2+3)`). Do not use `eval`.

        Constraints:
        - 1 <= s.length <= 3 * 10^5, the expression is valid, results fit in a 32-bit integer
        """, "calculate(s:string)->int",
      [("1 + 1",), (" 2-1 + 2 ",), ("(1+(4+5+2)-3)+(6+8)",), ("- (3 + (4 + 5))",), ("2147483647",), ("1-(     -2)",)],
      """
      class Solution:
          def calculate(self, s):
              res = 0; num = 0; sign = 1; st = []
              for c in s:
                  if c.isdigit():
                      num = num * 10 + int(c)
                  elif c in '+-':
                      res += sign * num; num = 0; sign = 1 if c == '+' else -1
                  elif c == '(':
                      st.append((res, sign)); res = 0; sign = 1
                  elif c == ')':
                      res += sign * num; num = 0
                      prev, sg = st.pop(); res = prev + sg * res
              return res + sign * num
      """, hint="On '(' push the running result and sign; on ')' combine."),
]

L_BSEARCH = [
    F("Search Insert Position", 35, "Easy", """
        In a sorted array of distinct integers, return the index of `target` if present, otherwise the index where it would be inserted to keep the array sorted. Aim for O(log n).

        Constraints:
        - 1 <= nums.length <= 10^4
        """, "searchInsert(nums:int[], target:int)->int",
      [([1, 3, 5, 6], 5), ([1, 3, 5, 6], 2), ([1, 3, 5, 6], 7), ([1], 0), ([1, 3], 3), ([1, 3, 5, 6], 0)],
      """
      class Solution:
          def searchInsert(self, nums, target):
              return bisect_left(nums, target)
      """, hint="Lower-bound binary search."),
    F("Find Peak Element", 162, "Medium", """
        A peak is an element strictly greater than its neighbours (treat both ends as having a neighbour of negative infinity). Given `nums` where adjacent elements are different, return the index of **any** peak, in O(log n).

        Constraints:
        - 1 <= nums.length <= 1000
        """, "findPeakElement(nums:int[])->int",
      [([1, 2, 3, 1],), ([1, 2, 1, 3, 5, 6, 4],), ([1],), ([2, 1],), ([1, 2],), ([3, 4, 3, 2, 1],)],
      """
      class Solution:
          def findPeakElement(self, nums):
              l, r = 0, len(nums) - 1
              while l < r:
                  m = (l + r) // 2
                  if nums[m] < nums[m + 1]:
                      l = m + 1
                  else:
                      r = m
              return l
      """, cmp="peak", hint="If the next element is larger, a peak lies to the right; otherwise to the left (or here)."),
    F("Find First and Last Position of Element in Sorted Array", 34, "Medium", """
        `nums` is sorted in non-decreasing order. Return `[first, last]`, the first and last index of `target`, or `[-1, -1]` if it does not occur. Aim for O(log n).

        Constraints:
        - 0 <= nums.length <= 10^5
        """, "searchRange(nums:int[], target:int)->int[]",
      [([5, 7, 7, 8, 8, 10], 8), ([5, 7, 7, 8, 8, 10], 6), ([], 0), ([1], 1), ([2, 2], 2), ([1, 2, 3, 3, 3, 3, 4], 3)],
      """
      class Solution:
          def searchRange(self, nums, target):
              l = bisect_left(nums, target)
              if l == len(nums) or nums[l] != target:
                  return [-1, -1]
              return [l, bisect_right(nums, target) - 1]
      """, hint="Two binary searches: lower bound and upper bound."),
]

L_LIST = [
    F("Reverse Linked List II", 92, "Medium", """
        Reverse the nodes of the list from position `left` to position `right` (1-indexed) and return the head.

        Constraints:
        - 1 <= n <= 500, 1 <= left <= right <= n
        """, "reverseBetween(head:ListNode, left:int, right:int)->ListNode",
      [([1, 2, 3, 4, 5], 2, 4), ([5], 1, 1), ([1, 2], 1, 2), ([1, 2, 3], 1, 3), ([3, 5], 1, 1), ([1, 2, 3, 4, 5, 6], 3, 5)],
      """
      class Solution:
          def reverseBetween(self, head, left, right):
              d = ListNode(0, head); prev = d
              for _ in range(left - 1):
                  prev = prev.next
              cur = prev.next
              for _ in range(right - left):
                  nxt = cur.next; cur.next = nxt.next; nxt.next = prev.next; prev.next = nxt
              return d.next
      """, hint="Move the next node to the front of the segment, right - left times."),
    F("Remove Duplicates from Sorted List II", 82, "Medium", """
        Given a sorted linked list, delete every node whose value appears more than once, leaving only values that appear exactly once. Return the (still sorted) list.

        Constraints:
        - 0 <= n <= 300
        """, "deleteDuplicates(head:ListNode)->ListNode",
      [([1, 2, 3, 3, 4, 4, 5],), ([1, 1, 1, 2, 3],), ([],), ([1, 1],), ([1, 2, 3],), ([1, 1, 2, 2, 3],)],
      """
      class Solution:
          def deleteDuplicates(self, head):
              d = ListNode(0, head); prev = d
              while head:
                  if head.next and head.next.val == head.val:
                      while head.next and head.next.val == head.val:
                          head = head.next
                      prev.next = head.next
                  else:
                      prev = prev.next
                  head = head.next
              return d.next
      """, hint="A dummy head and a pointer to the last node you are sure to keep."),
    F("Rotate List", 61, "Medium", """
        Rotate the list to the right by `k` places and return the new head.

        Constraints:
        - 0 <= n <= 500, 0 <= k <= 2 * 10^9
        """, "rotateRight(head:ListNode, k:int)->ListNode",
      [([1, 2, 3, 4, 5], 2), ([0, 1, 2], 4), ([], 0), ([1], 99), ([1, 2], 0), ([1, 2, 3, 4, 5], 5)],
      """
      class Solution:
          def rotateRight(self, head, k):
              if not head or not head.next:
                  return head
              n = 1; tail = head
              while tail.next:
                  tail = tail.next; n += 1
              k %= n
              if k == 0:
                  return head
              tail.next = head; new_tail = head
              for _ in range(n - k - 1):
                  new_tail = new_tail.next
              nh = new_tail.next; new_tail.next = None
              return nh
      """, hint="Make the list a ring, then cut it at the right spot."),
    F("Partition List", 86, "Medium", """
        Rearrange the list so that all nodes with value less than `x` come before nodes with value greater than or equal to `x`, preserving the original relative order within each part.

        Constraints:
        - 0 <= n <= 200
        """, "partition(head:ListNode, x:int)->ListNode",
      [([1, 4, 3, 2, 5, 2], 3), ([2, 1], 2), ([], 0), ([1], 0), ([3, 1, 2], 4), ([5, 4, 3, 2, 1], 3)],
      """
      class Solution:
          def partition(self, head, x):
              a = da = ListNode(); b = db = ListNode()
              while head:
                  if head.val < x:
                      a.next = head; a = a.next
                  else:
                      b.next = head; b = b.next
                  head = head.next
              b.next = None; a.next = db.next
              return da.next
      """, hint="Build two lists (smaller / not smaller) and join them."),
]

L_DESIGN = [
    D("Insert Delete GetRandom O(1)", 380, "Medium", """
        Implement a set that supports insert, remove and random access in average O(1) time.

        - `insert(val)` adds `val` if absent and returns `true`; returns `false` if it was already present.
        - `remove(val)` removes `val` if present and returns `true`; otherwise `false`.
        - `getRandom()` returns a uniformly random element from the current set.

        The tests only call `getRandom` while the set holds exactly one element, so the output is deterministic.
        """, "RandomizedSet", "", ["insert(val:int)->bool", "remove(val:int)->bool", "getRandom()->int"],
      [[("RandomizedSet", []), ("insert", [1]), ("remove", [2]), ("insert", [2]), ("remove", [1]), ("insert", [2]), ("getRandom", [])],
       [("RandomizedSet", []), ("insert", [-5]), ("insert", [-5]), ("getRandom", []), ("remove", [-5]), ("remove", [-5]), ("insert", [7]), ("getRandom", [])],
       [("RandomizedSet", [])] + [("insert", [i]) for i in range(100)] + [("remove", [i]) for i in range(100) if i != 42] + [("insert", [42]), ("getRandom", [])]],
      """
      class RandomizedSet:
          def __init__(self):
              self.a = []; self.pos = {}
          def insert(self, val):
              if val in self.pos:
                  return False
              self.pos[val] = len(self.a); self.a.append(val); return True
          def remove(self, val):
              if val not in self.pos:
                  return False
              i = self.pos.pop(val); last = self.a.pop()
              if i < len(self.a):
                  self.a[i] = last; self.pos[last] = i
              return True
          def getRandom(self):
              return random.choice(self.a)
      """, hint="An array for random access plus a map value -> index; remove by swapping with the last element."),
]
