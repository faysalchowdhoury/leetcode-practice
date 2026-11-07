from dsl import F, D, R

G05 = [
    F("Valid Parentheses", 20, "Easy", """
        A string made only of `()[]{}` is valid if every opening bracket is closed by the same type of bracket, in the correct order. Return `true` if `s` is valid.

        Constraints:
        - 1 <= s.length <= 10^4
        """, "isValid(s:string)->bool",
      [("()",), ("()[]{}",), ("(]",), ("([)]",), ("{[]}",), ("(",), (")",), ("((()))[]{{}}",)],
      """
      class Solution:
          def isValid(self, s):
              st = []; pair = {')': '(', ']': '[', '}': '{'}
              for c in s:
                  if c in pair:
                      if not st or st.pop() != pair[c]:
                          return False
                  else:
                      st.append(c)
              return not st
      """, hint="Push openers; on a closer, the top of the stack must be its matching opener."),
    F("Evaluate Reverse Polish Notation", 150, "Medium", """
        `tokens` is an arithmetic expression in Reverse Polish Notation. Valid operators are `+`, `-`, `*`, `/`. Division truncates toward zero. Evaluate the expression and return the result as an integer.

        The expression is always valid and every intermediate result fits in a 32-bit integer.

        Constraints:
        - 1 <= tokens.length <= 10^4
        """, "evalRPN(tokens:string[])->int",
      [(["2", "1", "+", "3", "*"],), (["4", "13", "5", "/", "+"],), (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],), (["3", "-4", "*"],), (["7", "-2", "/"],), (["18"],), (["-7", "2", "/"],)],
      """
      class Solution:
          def evalRPN(self, tokens):
              st = []
              for t in tokens:
                  if t in '+-*/' and len(t) == 1:
                      b = st.pop(); a = st.pop()
                      st.append(a + b if t == '+' else a - b if t == '-' else a * b if t == '*' else int(a / b))
                  else:
                      st.append(int(t))
              return st[0]
      """, hint="Numbers go on a stack; an operator pops two numbers and pushes the result."),
    F("Daily Temperatures", 739, "Medium", """
        Given daily `temperatures`, return an array `answer` where `answer[i]` is the number of days you must wait after day `i` for a warmer temperature, or 0 if there is none.

        Constraints:
        - 1 <= temperatures.length <= 10^5
        - 30 <= temperatures[i] <= 100
        """, "dailyTemperatures(temperatures:int[])->int[]",
      [([73, 74, 75, 71, 69, 72, 76, 73],), ([30, 40, 50, 60],), ([30, 60, 90],), ([90, 80, 70],), ([50],), ([55, 38, 53, 81, 61, 97, 35, 44],)],
      """
      class Solution:
          def dailyTemperatures(self, temperatures):
              res = [0] * len(temperatures); st = []
              for i, t in enumerate(temperatures):
                  while st and temperatures[st[-1]] < t:
                      j = st.pop(); res[j] = i - j
                  st.append(i)
              return res
      """, hint="Monotonic decreasing stack of indices: pop everything colder than today."),
    F("Car Fleet", 853, "Medium", """
        Cars drive to a destination `target` miles away along a one-lane road. Car `i` starts at `position[i]` with constant `speed[i]`. A car cannot pass another; it slows down and joins the fleet in front of it, then they move together at the slower speed.

        Return the number of fleets that arrive at the destination. (A fleet can be a single car; cars that catch up exactly at the destination count as one fleet.)

        Constraints:
        - n == position.length == speed.length, 1 <= n <= 10^5
        - 0 <= position[i] < target <= 10^6, positions are distinct
        """, "carFleet(target:int, position:int[], speed:int[])->int",
      [(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]), (10, [3], [3]), (100, [0, 2, 4], [4, 2, 1]), (10, [6, 8], [3, 2]), (20, [6, 2, 17, 9], [7, 5, 2, 3]), (10, [0, 4, 2], [2, 1, 3])],
      """
      class Solution:
          def carFleet(self, target, position, speed):
              cars = sorted(zip(position, speed), reverse=True)
              fleets = 0; slowest = 0.0
              for p, s in cars:
                  t = (target - p) / s
                  if t > slowest:
                      fleets += 1; slowest = t
              return fleets
      """, hint="Sort by starting position, closest to target first, and compare arrival times."),
    F("Largest Rectangle in Histogram", 84, "Hard", """
        Given bar heights `heights` of a histogram where each bar has width 1, return the area of the largest rectangle in the histogram.

        Constraints:
        - 1 <= heights.length <= 10^5
        - 0 <= heights[i] <= 10^4
        """, "largestRectangleArea(heights:int[])->int",
      [([2, 1, 5, 6, 2, 3],), ([2, 4],), ([1],), ([2, 1, 2],), ([6, 2, 5, 4, 5, 1, 6],), ([0, 9],), ([1, 1, 1, 1],)],
      """
      class Solution:
          def largestRectangleArea(self, heights):
              st = []; best = 0
              hs = heights + [0]
              for i, h in enumerate(hs):
                  start = i
                  while st and st[-1][1] >= h:
                      idx, hh = st.pop(); best = max(best, hh * (i - idx)); start = idx
                  st.append((start, h))
              return best
      """, hint="Keep a stack of increasing bars; when a shorter bar arrives, finish the taller ones."),
    F("Sliding Window Maximum", 239, "Hard", """
        A window of size `k` slides from the left of `nums` to the right, one position at a time. Return the maximum of each window position.

        Constraints:
        - 1 <= k <= nums.length <= 10^5
        - -10^4 <= nums[i] <= 10^4
        """, "maxSlidingWindow(nums:int[], k:int)->int[]",
      [([1, 3, -1, -3, 5, 3, 6, 7], 3), ([1], 1), ([9, 11], 2), ([4, 3, 2, 1], 2), ([1, -1], 1), ([7, 2, 4], 2), (list(range(3000)), 50)],
      """
      class Solution:
          def maxSlidingWindow(self, nums, k):
              dq = deque(); res = []
              for i, x in enumerate(nums):
                  while dq and nums[dq[-1]] <= x:
                      dq.pop()
                  dq.append(i)
                  if dq[0] <= i - k:
                      dq.popleft()
                  if i >= k - 1:
                      res.append(nums[dq[0]])
              return res
      """, hint="A deque of indices whose values are decreasing; the front is always the window maximum."),
]

G06 = [
    F("Binary Search", 704, "Easy", """
        Given a sorted (ascending) array `nums` of distinct integers and a `target`, return the index of `target` or -1 if it is not present. Aim for O(log n).

        Constraints:
        - 1 <= nums.length <= 10^4
        """, "search(nums:int[], target:int)->int",
      [([-1, 0, 3, 5, 9, 12], 9), ([-1, 0, 3, 5, 9, 12], 2), ([5], 5), ([5], -5), ([1, 2, 3, 4, 5, 6, 7], 1), ([1, 2, 3, 4, 5, 6, 7], 7)],
      """
      class Solution:
          def search(self, nums, target):
              l, r = 0, len(nums) - 1
              while l <= r:
                  m = (l + r) // 2
                  if nums[m] == target:
                      return m
                  if nums[m] < target:
                      l = m + 1
                  else:
                      r = m - 1
              return -1
      """, hint="Halve the search range every step."),
    F("Search a 2D Matrix", 74, "Medium", """
        `matrix` has rows sorted left to right, and the first number of each row is greater than the last number of the previous row. Return `true` if `target` is in the matrix. Aim for O(log(m*n)).

        Constraints:
        - 1 <= m, n <= 100
        """, "searchMatrix(matrix:int[][], target:int)->bool",
      [([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3), ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13), ([[1]], 1), ([[1]], 2), ([[1, 3]], 3), ([[1], [3]], 3), ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 60)],
      """
      class Solution:
          def searchMatrix(self, matrix, target):
              m, n = len(matrix), len(matrix[0]); l, r = 0, m * n - 1
              while l <= r:
                  mid = (l + r) // 2; v = matrix[mid // n][mid % n]
                  if v == target:
                      return True
                  if v < target:
                      l = mid + 1
                  else:
                      r = mid - 1
              return False
      """, hint="Treat the matrix as one sorted array of length m*n."),
    F("Koko Eating Bananas", 875, "Medium", """
        There are piles of bananas `piles[i]` and `h` hours. Each hour Koko picks one pile and eats up to `k` bananas from it (finishing the pile early wastes the rest of that hour). Return the smallest integer `k` that lets her finish all piles within `h` hours.

        Constraints:
        - 1 <= piles.length <= h <= 10^9 (piles.length <= 10^4)
        - 1 <= piles[i] <= 10^9
        """, "minEatingSpeed(piles:int[], h:int)->int",
      [([3, 6, 7, 11], 8), ([30, 11, 23, 4, 20], 5), ([30, 11, 23, 4, 20], 6), ([1], 1), ([1000000000], 2), ([312884470], 968709470), ([805306368, 805306368, 805306368], 1000000000)],
      """
      class Solution:
          def minEatingSpeed(self, piles, h):
              l, r = 1, max(piles)
              while l < r:
                  m = (l + r) // 2
                  if sum((p + m - 1) // m for p in piles) <= h:
                      r = m
                  else:
                      l = m + 1
              return l
      """, hint="Binary search on the answer k, checking feasibility with a simple loop."),
    F("Find Minimum in Rotated Sorted Array", 153, "Medium", """
        A sorted array of unique integers was rotated between 1 and n times. Given the rotated array `nums`, return its minimum element in O(log n).

        Constraints:
        - 1 <= nums.length <= 5000
        """, "findMin(nums:int[])->int",
      [([3, 4, 5, 1, 2],), ([4, 5, 6, 7, 0, 1, 2],), ([11, 13, 15, 17],), ([2, 1],), ([1],), ([5, 1, 2, 3, 4],)],
      """
      class Solution:
          def findMin(self, nums):
              l, r = 0, len(nums) - 1
              while l < r:
                  m = (l + r) // 2
                  if nums[m] > nums[r]:
                      l = m + 1
                  else:
                      r = m
              return nums[l]
      """, hint="Compare the middle with the right end to decide which half contains the drop."),
    F("Search in Rotated Sorted Array", 33, "Medium", """
        A sorted array of distinct integers was rotated at an unknown pivot. Return the index of `target` in `nums`, or -1 if absent, in O(log n).

        Constraints:
        - 1 <= nums.length <= 5000
        """, "search(nums:int[], target:int)->int",
      [([4, 5, 6, 7, 0, 1, 2], 0), ([4, 5, 6, 7, 0, 1, 2], 3), ([1], 0), ([1], 1), ([3, 1], 1), ([5, 1, 3], 5), ([6, 7, 1, 2, 3, 4, 5], 4)],
      """
      class Solution:
          def search(self, nums, target):
              l, r = 0, len(nums) - 1
              while l <= r:
                  m = (l + r) // 2
                  if nums[m] == target:
                      return m
                  if nums[l] <= nums[m]:
                      if nums[l] <= target < nums[m]:
                          r = m - 1
                      else:
                          l = m + 1
                  else:
                      if nums[m] < target <= nums[r]:
                          l = m + 1
                      else:
                          r = m - 1
              return -1
      """, hint="One half around the midpoint is always sorted; check whether the target falls inside it."),
    D("Time Based Key-Value Store", 981, "Medium", """
        Design a key-value store that can store several values for the same key at different timestamps and retrieve the value at a given time.

        - `TimeMap()` creates the object.
        - `set(key, value, timestamp)` stores `value` for `key` at `timestamp`.
        - `get(key, timestamp)` returns the value stored with the largest `timestamp_prev <= timestamp`, or `""` if there is none.

        Timestamps passed to `set` are strictly increasing for each key.
        """, "TimeMap", "", ["set(key:string, value:string, timestamp:int)->void", "get(key:string, timestamp:int)->string"],
      [[("TimeMap", []), ("set", ["foo", "bar", 1]), ("get", ["foo", 1]), ("get", ["foo", 3]), ("set", ["foo", "bar2", 4]), ("get", ["foo", 4]), ("get", ["foo", 5])],
       [("TimeMap", []), ("set", ["a", "x", 10]), ("get", ["a", 5]), ("get", ["b", 10]), ("set", ["b", "y", 3]), ("get", ["b", 100]), ("get", ["a", 10])],
       [("TimeMap", [])] + [("set", ["k", "v%d" % i, i * 2]) for i in range(1, 300)] + [("get", ["k", t]) for t in (1, 2, 3, 100, 101, 597, 598, 599, 10000)]],
      """
      class TimeMap:
          def __init__(self):
              self.d = defaultdict(list)
          def set(self, key, value, timestamp):
              self.d[key].append((timestamp, value))
          def get(self, key, timestamp):
              a = self.d.get(key, [])
              i = bisect_right(a, (timestamp, chr(0x10ffff)))
              return a[i - 1][1] if i else ""
      """, hint="Each key's list is already sorted by time, so binary search it."),
    F("Median of Two Sorted Arrays", 4, "Hard", """
        Given two sorted arrays `nums1` and `nums2`, return the median of the combined values. The overall run time should be O(log(m+n)).

        Constraints:
        - 0 <= m, n <= 1000, 1 <= m + n <= 2000
        """, "findMedianSortedArrays(nums1:int[], nums2:int[])->double",
      [([1, 3], [2]), ([1, 2], [3, 4]), ([], [1]), ([0, 0], [0, 0]), ([2], []), ([1, 3, 5, 7], [2, 4, 6, 8, 10]), ([-5, 3, 6, 12, 15], [-12, -10, -6, -3, 4, 10])],
      """
      class Solution:
          def findMedianSortedArrays(self, nums1, nums2):
              a, b = nums1, nums2
              if len(a) > len(b):
                  a, b = b, a
              total = len(a) + len(b); half = total // 2
              l, r = 0, len(a)
              while True:
                  i = (l + r) // 2; j = half - i
                  al = a[i - 1] if i > 0 else -inf; ar = a[i] if i < len(a) else inf
                  bl = b[j - 1] if j > 0 else -inf; br = b[j] if j < len(b) else inf
                  if al <= br and bl <= ar:
                      if total % 2:
                          return float(min(ar, br))
                      return (max(al, bl) + min(ar, br)) / 2
                  if al > br:
                      r = i - 1
                  else:
                      l = i + 1
      """, cmp="float", hint="Binary search the partition point of the smaller array."),
]

G07 = [
    F("Reverse Linked List", 206, "Easy", """
        Given the head of a singly linked list, reverse the list and return the new head.

        Constraints:
        - 0 <= number of nodes <= 5000
        """, "reverseList(head:ListNode)->ListNode",
      [([1, 2, 3, 4, 5],), ([1, 2],), ([],), ([1],), ([5, 4, 3, 2, 1, 0],)],
      """
      class Solution:
          def reverseList(self, head):
              prev = None
              while head:
                  nxt = head.next; head.next = prev; prev = head; head = nxt
              return prev
      """, hint="Walk the list once, pointing each node at the one behind it."),
    F("Merge Two Sorted Lists", 21, "Easy", """
        Merge two sorted linked lists into one sorted list made by splicing together the nodes of the inputs, and return its head.

        Constraints:
        - 0 <= length of each list <= 50
        """, "mergeTwoLists(list1:ListNode, list2:ListNode)->ListNode",
      [([1, 2, 4], [1, 3, 4]), ([], []), ([], [0]), ([1, 3, 5], [2, 4, 6, 8, 10]), ([5], [1, 2, 4]), ([-3, 0, 0], [-3, -1, 7])],
      """
      class Solution:
          def mergeTwoLists(self, list1, list2):
              d = t = ListNode()
              while list1 and list2:
                  if list1.val <= list2.val:
                      t.next = list1; list1 = list1.next
                  else:
                      t.next = list2; list2 = list2.next
                  t = t.next
              t.next = list1 or list2
              return d.next
      """, hint="A dummy head node removes the special case for the first element."),
    F("Reorder List", 143, "Medium", """
        Reorder the list `L0 -> L1 -> ... -> Ln` in place into `L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...`. Do not change node values, only the links.

        Constraints:
        - 1 <= number of nodes <= 5 * 10^4
        """, "reorderList(head:ListNode)->void",
      [([1, 2, 3, 4],), ([1, 2, 3, 4, 5],), ([1],), ([1, 2],), ([1, 2, 3],), ([1, 2, 3, 4, 5, 6],)],
      """
      class Solution:
          def reorderList(self, head):
              slow, fast = head, head.next
              while fast and fast.next:
                  slow = slow.next; fast = fast.next.next
              second = slow.next; slow.next = None; prev = None
              while second:
                  nxt = second.next; second.next = prev; prev = second; second = nxt
              first, second = head, prev
              while second:
                  a, b = first.next, second.next
                  first.next = second; second.next = a
                  first, second = a, b
      """, inplace="head", hint="Find the middle, reverse the second half, then interleave the two halves."),
    F("Remove Nth Node From End of List", 19, "Medium", """
        Remove the `n`-th node from the end of the list and return its head.

        Constraints:
        - 1 <= list length <= 30, 1 <= n <= list length
        """, "removeNthFromEnd(head:ListNode, n:int)->ListNode",
      [([1, 2, 3, 4, 5], 2), ([1], 1), ([1, 2], 1), ([1, 2], 2), ([1, 2, 3], 3), ([1, 2, 3, 4, 5, 6], 6)],
      """
      class Solution:
          def removeNthFromEnd(self, head, n):
              d = ListNode(0, head); fast = slow = d
              for _ in range(n):
                  fast = fast.next
              while fast.next:
                  fast = fast.next; slow = slow.next
              slow.next = slow.next.next
              return d.next
      """, hint="Two pointers n nodes apart; when the front one reaches the end, the back one is just before the target."),
    F("Add Two Numbers", 2, "Medium", """
        Two non-empty linked lists represent two non-negative integers with digits stored in **reverse order** (head is the ones digit). Add the numbers and return the sum as a linked list in the same format.

        Constraints:
        - 1 <= length of each list <= 100, digits 0-9, no leading zeros except the number 0 itself
        """, "addTwoNumbers(l1:ListNode, l2:ListNode)->ListNode",
      [([2, 4, 3], [5, 6, 4]), ([0], [0]), ([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9]), ([1], [9, 9]), ([5], [5]), ([1, 8], [0])],
      """
      class Solution:
          def addTwoNumbers(self, l1, l2):
              d = t = ListNode(); carry = 0
              while l1 or l2 or carry:
                  s = carry + (l1.val if l1 else 0) + (l2.val if l2 else 0)
                  carry, digit = divmod(s, 10)
                  t.next = ListNode(digit); t = t.next
                  l1 = l1.next if l1 else None; l2 = l2.next if l2 else None
              return d.next
      """, hint="Schoolbook addition with a carry; keep going while either list or the carry remains."),
    F("Reverse Nodes in k-Group", 25, "Hard", """
        Reverse the nodes of the list `k` at a time and return the modified list. If the number of remaining nodes is less than `k`, leave them as they are. Only node links may change, not values.

        Constraints:
        - 1 <= k <= n <= 5000
        """, "reverseKGroup(head:ListNode, k:int)->ListNode",
      [([1, 2, 3, 4, 5], 2), ([1, 2, 3, 4, 5], 3), ([1], 1), ([1, 2, 3, 4], 4), ([1, 2, 3, 4, 5, 6, 7], 3), ([1, 2], 1)],
      """
      class Solution:
          def reverseKGroup(self, head, k):
              d = ListNode(0, head); prev = d
              while True:
                  kth = prev
                  for _ in range(k):
                      kth = kth.next
                      if not kth:
                          return d.next
                  nxt = kth.next
                  cur, p = prev.next, nxt
                  while cur is not nxt:
                      t = cur.next; cur.next = p; p = cur; cur = t
                  tmp = prev.next; prev.next = kth; prev = tmp
      """, hint="Check that k nodes exist, reverse exactly that segment, reconnect, repeat."),
    F("Copy List with Random Pointer", 138, "Medium", """
        Each node of a linked list has a `next` pointer and an extra `random` pointer that may point to any node in the list or be null. Return a deep copy of the list: all new nodes, with the same shape of `next` and `random` links.

        In the tests, a list is shown as `[[val, randomIndex], ...]`, where `randomIndex` is the index of the node `random` points to (or `null`).

        Constraints:
        - 0 <= n <= 1000
        """, "copyRandomList(head:RandomList)->RandomList",
      [([[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],), ([[1, 1], [2, 1]],), ([[3, None], [3, 0], [3, None]],), ([],), ([[1, None]],), ([[1, 0]],)],
      """
      class Solution:
          def copyRandomList(self, head):
              m = {None: None}; n = head
              while n:
                  m[n] = Node(n.val); n = n.next
              n = head
              while n:
                  m[n].next = m[n.next]; m[n].random = m[n.random]; n = n.next
              return m[head]
      """, hint="Map every original node to its copy first, then wire up next and random."),
]

G08 = [
    F("Linked List Cycle", 141, "Easy", """
        Return `true` if the linked list contains a cycle (some node can be reached again by following `next`).

        In the tests the input is shown as `[values, pos]`, where `pos` is the index the tail's `next` points back to (-1 means no cycle).

        Constraints:
        - 0 <= number of nodes <= 10^4
        """, "hasCycle(head:CycleList)->bool",
      [([[3, 2, 0, -4], 1],), ([[1, 2], 0],), ([[1], -1],), ([[], -1],), ([[1, 2, 3, 4, 5], -1],), ([[1, 2, 3, 4, 5], 4],), ([[1], 0],)],
      """
      class Solution:
          def hasCycle(self, head):
              slow = fast = head
              while fast and fast.next:
                  slow = slow.next; fast = fast.next.next
                  if slow is fast:
                      return True
              return False
      """, hint="A fast and a slow pointer will meet inside a cycle."),
    F("Find the Duplicate Number", 287, "Medium", """
        `nums` has `n + 1` integers, each in the range `[1, n]`, and exactly one value is repeated (possibly several times). Return the repeated number without modifying `nums` and using only constant extra space.

        Constraints:
        - 1 <= n <= 10^5
        """, "findDuplicate(nums:int[])->int",
      [([1, 3, 4, 2, 2],), ([3, 1, 3, 4, 2],), ([3, 3, 3, 3, 3],), ([1, 1],), ([2, 5, 9, 6, 9, 3, 8, 9, 7, 1],), ([1, 4, 4, 2, 4],)],
      """
      class Solution:
          def findDuplicate(self, nums):
              slow = fast = 0
              while True:
                  slow = nums[slow]; fast = nums[nums[fast]]
                  if slow == fast:
                      break
              slow2 = 0
              while slow != slow2:
                  slow = nums[slow]; slow2 = nums[slow2]
              return slow
      """, hint="Treat index -> nums[index] as a linked list; the duplicate is where the cycle starts."),
    F("Happy Number", 202, "Easy", """
        Replace a number by the sum of the squares of its digits and repeat. If the process reaches 1, the number is happy; if it loops forever without reaching 1, it is not. Return `true` if `n` is happy.

        Constraints:
        - 1 <= n <= 2^31 - 1
        """, "isHappy(n:int)->bool",
      [(19,), (2,), (1,), (7,), (4,), (100,), (1111111,), (2147483647,)],
      """
      class Solution:
          def isHappy(self, n):
              seen = set()
              while n != 1 and n not in seen:
                  seen.add(n); n = sum(int(d) ** 2 for d in str(n))
              return n == 1
      """, hint="Detect the loop with a set, or with fast and slow pointers on the sequence."),
]

G09 = [
    D("Min Stack", 155, "Medium", """
        Design a stack that supports `push`, `pop`, `top` and retrieving the minimum element, all in O(1) time.

        - `push(val)` pushes `val` onto the stack.
        - `pop()` removes the top element.
        - `top()` returns the top element.
        - `getMin()` returns the minimum element currently in the stack.

        `pop`, `top` and `getMin` are only called on a non-empty stack.
        """, "MinStack", "", ["push(val:int)->void", "pop()->void", "top()->int", "getMin()->int"],
      [[("MinStack", []), ("push", [-2]), ("push", [0]), ("push", [-3]), ("getMin", []), ("pop", []), ("top", []), ("getMin", [])],
       [("MinStack", []), ("push", [1]), ("push", [1]), ("push", [1]), ("getMin", []), ("pop", []), ("getMin", []), ("pop", []), ("getMin", [])],
       [("MinStack", [])] + [("push", [(i * 37) % 101 - 50]) for i in range(200)] + [x for _ in range(100) for x in (("getMin", []), ("top", []), ("pop", []))]],
      """
      class MinStack:
          def __init__(self):
              self.s = []; self.m = []
          def push(self, val):
              self.s.append(val); self.m.append(min(val, self.m[-1]) if self.m else val)
          def pop(self):
              self.s.pop(); self.m.pop()
          def top(self):
              return self.s[-1]
          def getMin(self):
              return self.m[-1]
      """, hint="Store the running minimum next to every element."),
    D("LRU Cache", 146, "Medium", """
        Design a Least Recently Used cache with a fixed capacity.

        - `LRUCache(capacity)` creates the cache.
        - `get(key)` returns the value if the key exists, otherwise -1. A successful get makes the key the most recently used.
        - `put(key, value)` inserts or updates the key. If the cache is over capacity afterwards, evict the least recently used key.

        Both operations should run in O(1) average time.
        """, "LRUCache", "capacity:int", ["get(key:int)->int", "put(key:int, value:int)->void"],
      [[("LRUCache", [2]), ("put", [1, 1]), ("put", [2, 2]), ("get", [1]), ("put", [3, 3]), ("get", [2]), ("put", [4, 4]), ("get", [1]), ("get", [3]), ("get", [4])],
       [("LRUCache", [1]), ("put", [2, 1]), ("get", [2]), ("put", [3, 2]), ("get", [2]), ("get", [3])],
       [("LRUCache", [2]), ("put", [2, 1]), ("put", [2, 2]), ("get", [2]), ("put", [1, 1]), ("put", [4, 1]), ("get", [2])],
       [("LRUCache", [50])] + [(("put", [(i * 7) % 120, i]) if i % 3 else ("get", [(i * 11) % 120])) for i in range(600)]],
      """
      class LRUCache:
          def __init__(self, capacity):
              self.c = OrderedDict(); self.cap = capacity
          def get(self, key):
              if key not in self.c:
                  return -1
              self.c.move_to_end(key); return self.c[key]
          def put(self, key, value):
              self.c[key] = value; self.c.move_to_end(key)
              if len(self.c) > self.cap:
                  self.c.popitem(last=False)
      """, hint="A hash map plus a doubly linked list gives O(1) lookups and O(1) reordering."),
    D("Design Twitter", 355, "Medium", """
        Design a simplified Twitter where users can post tweets, follow/unfollow others, and see the 10 most recent tweet ids in their news feed.

        - `postTweet(userId, tweetId)` composes a new tweet.
        - `getNewsFeed(userId)` returns up to the 10 most recent tweet ids from the user and the people they follow, newest first.
        - `follow(followerId, followeeId)` / `unfollow(followerId, followeeId)` update who follows whom.

        Tweet ids are unique.
        """, "Twitter", "", ["postTweet(userId:int, tweetId:int)->void", "getNewsFeed(userId:int)->int[]", "follow(followerId:int, followeeId:int)->void", "unfollow(followerId:int, followeeId:int)->void"],
      [[("Twitter", []), ("postTweet", [1, 5]), ("getNewsFeed", [1]), ("follow", [1, 2]), ("postTweet", [2, 6]), ("getNewsFeed", [1]), ("unfollow", [1, 2]), ("getNewsFeed", [1])],
       [("Twitter", [])] + [("postTweet", [1, i]) for i in range(1, 13)] + [("getNewsFeed", [1])],
       [("Twitter", []), ("postTweet", [1, 1]), ("follow", [2, 1]), ("follow", [2, 3]), ("postTweet", [3, 2]), ("postTweet", [2, 3]), ("getNewsFeed", [2]), ("unfollow", [2, 1]), ("getNewsFeed", [2]), ("follow", [2, 2]), ("unfollow", [2, 2]), ("getNewsFeed", [2])]],
      """
      class Twitter:
          def __init__(self):
              self.t = 0; self.tweets = defaultdict(list); self.f = defaultdict(set)
          def postTweet(self, userId, tweetId):
              self.t += 1; self.tweets[userId].append((self.t, tweetId))
          def getNewsFeed(self, userId):
              users = self.f[userId] | {userId}
              allt = [x for u in users for x in self.tweets[u]]
              return [tid for _, tid in sorted(allt, reverse=True)[:10]]
          def follow(self, followerId, followeeId):
              if followerId != followeeId:
                  self.f[followerId].add(followeeId)
          def unfollow(self, followerId, followeeId):
              self.f[followerId].discard(followeeId)
      """, hint="Give each tweet a global timestamp; merge the recent tweets of followed users, e.g. with a heap."),
    D("Detect Squares", 2013, "Medium", """
        Design a data structure that stores a stream of 2D points (duplicates allowed) and counts axis-aligned squares with positive area.

        - `add(point)` adds a point `[x, y]`.
        - `count(point)` returns the number of ways to choose three stored points that, together with the query point, form an axis-aligned square with positive area. Points of the same value stored twice count as different choices.
        """, "DetectSquares", "", ["add(point:int[])->void", "count(point:int[])->int"],
      [[("DetectSquares", []), ("add", [[3, 10]]), ("add", [[11, 2]]), ("add", [[3, 2]]), ("count", [[11, 10]]), ("count", [[14, 8]]), ("add", [[11, 2]]), ("count", [[11, 10]])],
       [("DetectSquares", []), ("count", [[0, 0]]), ("add", [[0, 0]]), ("add", [[0, 5]]), ("add", [[5, 0]]), ("add", [[5, 5]]), ("count", [[0, 0]]), ("count", [[5, 5]]), ("count", [[2, 2]])],
       [("DetectSquares", [])] + [("add", [[(i * 3) % 10, (i * 7) % 10]]) for i in range(60)] + [("count", [[x, y]]) for x in range(0, 10, 3) for y in range(0, 10, 4)]],
      """
      class DetectSquares:
          def __init__(self):
              self.cnt = Counter(); self.pts = []
          def add(self, point):
              p = tuple(point); self.cnt[p] += 1; self.pts.append(p)
          def count(self, point):
              x, y = point; res = 0
              for px, py in self.cnt:
                  if abs(px - x) == abs(py - y) and px != x:
                      res += self.cnt[(px, py)] * self.cnt.get((px, y), 0) * self.cnt.get((x, py), 0)
              return res
      """, hint="Store counts per point; for a query, try every stored point as the diagonal corner."),
]
