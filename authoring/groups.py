"""The 31 pattern groups and which of the 223 problems sit in each.

Tags: B = on both the NeetCode 150 and LeetCode Top Interview 150 lists, N = NeetCode only, L = LeetCode only.
"""
import pr_a, pr_b, pr_c, pr_d, pr_e, pr_f1, pr_f2


def _collect(*mods):
    d = {}
    for m in mods:
        for name in dir(m):
            v = getattr(m, name)
            if isinstance(v, list) and v and isinstance(v[0], dict) and 'title' in v[0]:
                for p in v:
                    assert p['title'] not in d, 'duplicate title ' + p['title']
                    d[p['title']] = p
    return d


ALL = _collect(pr_a, pr_b, pr_c, pr_d, pr_e, pr_f1, pr_f2)

SPEC = [
    ("Hash map / set", "Trade memory for speed: remember what you have seen in a set or dictionary so each lookup is O(1).", [
        ("Contains Duplicate", "N"), ("Contains Duplicate II", "L"), ("Valid Anagram", "B"), ("Two Sum", "B"), ("Group Anagrams", "B"),
        ("Longest Consecutive Sequence", "B"), ("Ransom Note", "L"), ("Isomorphic Strings", "L"), ("Word Pattern", "L")]),
    ("Greedy / running value", "Make the locally best choice, or carry one running value (min so far, farthest reach, current sum) through a single pass.", [
        ("Product of Array Except Self", "B"), ("Best Time to Buy and Sell Stock", "B"), ("Best Time to Buy and Sell Stock II", "L"), ("Maximum Subarray", "B"),
        ("Maximum Sum Circular Subarray", "L"), ("Jump Game", "B"), ("Jump Game II", "B"), ("Gas Station", "B"), ("Majority Element", "L"), ("H-Index", "L"),
        ("Candy", "L"), ("Hand of Straights", "N"), ("Merge Triplets to Form Target Triplet", "N"), ("Partition Labels", "N"), ("Valid Parenthesis String", "N")]),
    ("In-place array rewrite", "Use a read pointer and a write pointer (or work from the back) to rewrite an array without extra space.", [
        ("Merge Sorted Array", "L"), ("Remove Element", "L"), ("Remove Duplicates from Sorted Array", "L"), ("Remove Duplicates from Sorted Array II", "L"), ("Rotate Array", "L")]),
    ("Two pointers", "Two indices walking towards each other (or in tandem) over sorted or symmetric data.", [
        ("Valid Palindrome", "B"), ("Two Sum II - Input Array Is Sorted", "B"), ("3Sum", "B"), ("Container With Most Water", "B"), ("Trapping Rain Water", "B"), ("Is Subsequence", "L")]),
    ("Sliding window", "Keep a window [l, r] over the data; grow r, and shrink l whenever the window stops being valid.", [
        ("Longest Substring Without Repeating Characters", "B"), ("Minimum Window Substring", "B"), ("Longest Repeating Character Replacement", "N"),
        ("Permutation in String", "N"), ("Minimum Size Subarray Sum", "L"), ("Substring with Concatenation of All Words", "L")]),
    ("String simulation / parsing", "Careful step-by-step processing of text; most bugs are off-by-one or edge cases, so test small inputs by hand.", [
        ("Encode and Decode Strings", "N"), ("Roman to Integer", "L"), ("Integer to Roman", "L"), ("Length of Last Word", "L"), ("Longest Common Prefix", "L"),
        ("Reverse Words in a String", "L"), ("Zigzag Conversion", "L"), ("Find the Index of the First Occurrence in a String", "L"), ("Text Justification", "L")]),
    ("Stack (incl. monotonic)", "Last-in first-out for matching and nesting; a monotonic stack answers 'next greater / smaller element' in O(n).", [
        ("Valid Parentheses", "B"), ("Evaluate Reverse Polish Notation", "B"), ("Daily Temperatures", "N"), ("Car Fleet", "N"), ("Largest Rectangle in Histogram", "N"),
        ("Sliding Window Maximum", "N"), ("Simplify Path", "L"), ("Basic Calculator", "L")]),
    ("Binary search", "Halve the search space each step. Works on sorted data and on any monotonic yes/no condition (search the answer).", [
        ("Search a 2D Matrix", "B"), ("Search in Rotated Sorted Array", "B"), ("Find Minimum in Rotated Sorted Array", "B"), ("Median of Two Sorted Arrays", "B"),
        ("Binary Search", "N"), ("Koko Eating Bananas", "N"), ("Time Based Key-Value Store", "N"), ("Search Insert Position", "L"), ("Find Peak Element", "L"),
        ("Find First and Last Position of Element in Sorted Array", "L")]),
    ("Linked list rewiring", "Draw the pointers. A dummy head node and 'save next before you overwrite it' fix most bugs.", [
        ("Add Two Numbers", "B"), ("Merge Two Sorted Lists", "B"), ("Copy List with Random Pointer", "B"), ("Reverse Nodes in k-Group", "B"), ("Remove Nth Node From End of List", "B"),
        ("Reverse Linked List", "N"), ("Reorder List", "N"), ("Reverse Linked List II", "L"), ("Remove Duplicates from Sorted List II", "L"), ("Rotate List", "L"), ("Partition List", "L")]),
    ("Fast and slow pointers", "Two pointers moving at different speeds detect cycles and find midpoints.", [
        ("Linked List Cycle", "B"), ("Happy Number", "B"), ("Find the Duplicate Number", "N")]),
    ("Design", "Combine a hash map with another structure (list, heap, linked list) so every operation hits its target complexity.", [
        ("Min Stack", "B"), ("LRU Cache", "B"), ("Design Twitter", "N"), ("Detect Squares", "N"), ("Insert Delete GetRandom O(1)", "L")]),
    ("Tree DFS", "Recursion on left and right subtrees; decide what to pass down (a bound, a running sum) and what to return up (a height, a count).", [
        ("Invert Binary Tree", "B"), ("Maximum Depth of Binary Tree", "B"), ("Same Tree", "B"), ("Binary Tree Maximum Path Sum", "B"), ("Diameter of Binary Tree", "N"),
        ("Balanced Binary Tree", "N"), ("Subtree of Another Tree", "N"), ("Count Good Nodes in Binary Tree", "N"), ("Symmetric Tree", "L"), ("Path Sum", "L"),
        ("Sum Root to Leaf Numbers", "L"), ("Flatten Binary Tree to Linked List", "L"), ("Count Complete Tree Nodes", "L"), ("Lowest Common Ancestor of a Binary Tree", "L")]),
    ("Tree BFS", "A queue processed one level at a time: take len(queue) nodes per round.", [
        ("Binary Tree Level Order Traversal", "B"), ("Binary Tree Right Side View", "B"), ("Binary Tree Zigzag Level Order Traversal", "L"),
        ("Average of Levels in Binary Tree", "L"), ("Populating Next Right Pointers in Each Node II", "L")]),
    ("BST rules", "In-order traversal of a BST is sorted, and every node splits its range: use both facts.", [
        ("Validate Binary Search Tree", "B"), ("Kth Smallest Element in a BST", "B"), ("Lowest Common Ancestor of a Binary Search Tree", "N"),
        ("Minimum Absolute Difference in BST", "L"), ("Binary Search Tree Iterator", "L")]),
    ("Tree build / serialize", "Pick the root from one traversal, split the other traversal around it, and recurse.", [
        ("Construct Binary Tree from Preorder and Inorder Traversal", "B"), ("Serialize and Deserialize Binary Tree", "N"),
        ("Construct Binary Tree from Inorder and Postorder Traversal", "L"), ("Convert Sorted Array to Binary Search Tree", "L"), ("Construct Quad Tree", "L")]),
    ("Merge-based divide and conquer", "Split in halves, solve each, merge the sorted results.", [
        ("Merge k Sorted Lists", "B"), ("Sort List", "L")]),
    ("Trie", "A tree keyed by characters: shared prefixes share nodes, so prefix queries cost O(length).", [
        ("Implement Trie (Prefix Tree)", "B"), ("Design Add and Search Words Data Structure", "B"), ("Word Search II", "B")]),
    ("Heap / top-k", "A heap gives the smallest or largest item in O(log n). Keep a size-k heap for 'top k' questions.", [
        ("Kth Largest Element in an Array", "B"), ("Find Median from Data Stream", "B"), ("Top K Frequent Elements", "N"), ("Kth Largest Element in a Stream", "N"),
        ("Last Stone Weight", "N"), ("K Closest Points to Origin", "N"), ("Task Scheduler", "N"), ("IPO", "L"), ("Find K Pairs with Smallest Sums", "L")]),
    ("Backtracking", "Choose, explore, un-choose. Prune branches that cannot lead to a valid answer.", [
        ("Combination Sum", "B"), ("Permutations", "B"), ("Generate Parentheses", "B"), ("Word Search", "B"), ("Letter Combinations of a Phone Number", "B"),
        ("Subsets", "N"), ("Subsets II", "N"), ("Combination Sum II", "N"), ("Palindrome Partitioning", "N"), ("N-Queens", "N"), ("N-Queens II", "L"), ("Combinations", "L")]),
    ("Graph traversal (DFS/BFS)", "DFS to explore regions, BFS for fewest steps. Mark cells visited when you enqueue them.", [
        ("Number of Islands", "B"), ("Surrounded Regions", "B"), ("Clone Graph", "B"), ("Word Ladder", "B"), ("Max Area of Island", "N"), ("Walls and Gates", "N"),
        ("Rotting Oranges", "N"), ("Pacific Atlantic Water Flow", "N"), ("Evaluate Division", "L"), ("Snakes and Ladders", "L"), ("Minimum Genetic Mutation", "L")]),
    ("Topological sort", "Order nodes of a directed acyclic graph: repeatedly take nodes with no remaining prerequisites.", [
        ("Course Schedule", "B"), ("Course Schedule II", "B"), ("Alien Dictionary", "N")]),
    ("Union-Find", "Track which items are connected with near-O(1) union and find.", [
        ("Redundant Connection", "N"), ("Number of Connected Components in an Undirected Graph", "N"), ("Graph Valid Tree", "N")]),
    ("Weighted shortest path", "Dijkstra with a min-heap when weights are non-negative; Bellman-Ford when the number of edges is limited.", [
        ("Network Delay Time", "N"), ("Swim in Rising Water", "N"), ("Cheapest Flights Within K Stops", "N")]),
    ("MST and Euler path", "Minimum spanning trees (Prim / Kruskal) and Hierholzer's algorithm for paths that use every edge once.", [
        ("Min Cost to Connect All Points", "N"), ("Reconstruct Itinerary", "N")]),
    ("1-D DP", "Define dp[i] in words, write the recurrence from earlier states, and often keep only the last one or two values.", [
        ("Climbing Stairs", "B"), ("House Robber", "B"), ("Word Break", "B"), ("Coin Change", "B"), ("Longest Increasing Subsequence", "B"),
        ("Min Cost Climbing Stairs", "N"), ("House Robber II", "N"), ("Decode Ways", "N"), ("Maximum Product Subarray", "N"), ("Partition Equal Subset Sum", "N")]),
    ("Expand around center", "Treat every position (and gap) as a palindrome centre and expand outwards.", [
        ("Longest Palindromic Substring", "B"), ("Palindromic Substrings", "N")]),
    ("2-D DP", "Two indices (two strings, or a grid) define the state; fill the table in an order that respects dependencies.", [
        ("Interleaving String", "B"), ("Edit Distance", "B"), ("Unique Paths", "N"), ("Longest Common Subsequence", "N"), ("Best Time to Buy and Sell Stock with Cooldown", "N"),
        ("Coin Change II", "N"), ("Target Sum", "N"), ("Longest Increasing Path in a Matrix", "N"), ("Distinct Subsequences", "N"), ("Burst Balloons", "N"),
        ("Regular Expression Matching", "N"), ("Triangle", "L"), ("Minimum Path Sum", "L"), ("Unique Paths II", "L"), ("Best Time to Buy and Sell Stock III", "L"),
        ("Best Time to Buy and Sell Stock IV", "L"), ("Maximal Square", "L")]),
    ("Intervals", "Sort by start (or end), then sweep while merging or counting overlaps.", [
        ("Insert Interval", "B"), ("Merge Intervals", "B"), ("Non-overlapping Intervals", "N"), ("Meeting Rooms", "N"), ("Meeting Rooms II", "N"),
        ("Minimum Interval to Include Each Query", "N"), ("Summary Ranges", "L"), ("Minimum Number of Arrows to Burst Balloons", "L")]),
    ("Matrix manipulation", "Index arithmetic: transpose / reverse, boundary shrinking, or using the matrix itself to store markers.", [
        ("Valid Sudoku", "B"), ("Spiral Matrix", "B"), ("Rotate Image", "B"), ("Set Matrix Zeroes", "B"), ("Game of Life", "L")]),
    ("Math", "Digit by digit arithmetic, fast exponentiation, and overflow awareness.", [
        ("Plus One", "B"), ("Pow(x, n)", "B"), ("Multiply Strings", "N"), ("Reverse Integer", "N"), ("Palindrome Number", "L"),
        ("Factorial Trailing Zeroes", "L"), ("Sqrt(x)", "L"), ("Max Points on a Line", "L")]),
    ("Bit manipulation", "XOR cancels pairs, n & (n - 1) clears the lowest set bit, shifts move bits.", [
        ("Single Number", "B"), ("Number of 1 Bits", "B"), ("Reverse Bits", "B"), ("Counting Bits", "N"), ("Missing Number", "N"), ("Sum of Two Integers", "N"),
        ("Add Binary", "L"), ("Single Number II", "L"), ("Bitwise AND of Range", "L")]),
]

# a couple of titles differ slightly from the list's short names
ALIASES = {"Bitwise AND of Range": "Bitwise AND of Numbers Range"}

GROUPS = []
_used = set()
for name, tip, items in SPEC:
    probs = []
    for title, tag in items:
        title = ALIASES.get(title, title)
        p = ALL[title]  # KeyError here means a title in SPEC has no problem written for it
        assert title not in _used, 'listed twice: ' + title
        _used.add(title)
        p['tag'] = tag
        probs.append(p)
    GROUPS.append({'name': name, 'tip': tip, 'problems': probs})

_unused = sorted(set(ALL) - _used)
if _unused:
    raise SystemExit('Problems written but not in any group: %s' % _unused)
