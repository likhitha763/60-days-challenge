"""
Week 5 Sprint Challenge — All-in-One
======================================
Two medium algorithm problems, each with a brute-force baseline and an
optimized solution, tested and benchmarked.

1. Longest Substring Without Repeating Characters -- sliding window
2. Maximum Subarray Sum -- Kadane's algorithm

Run with: python sprint_week5_all_in_one.py
"""

import random
import time


# ===========================================================================
# Problem 1: Longest Substring Without Repeating Characters
# ===========================================================================

def substring_brute_force(s: str) -> int:
    """
    Genuinely naive: for every (start, end) pair, build that substring fresh
    and check for repeats via len(set(...)) == len(...). O(n^2) substrings,
    each costing O(n) to verify -> O(n^3) total.

    (A first draft of this function reused a running `seen` set across the
    inner loop and broke early on the first repeat -- that was accidentally
    closer to O(n^2) in practice, and with a small alphabet the early break
    made it look deceptively fast. This version is deliberately the slow,
    naive one so the complexity label matches the code.)
    """
    n = len(s)
    longest = 0
    for start in range(n):
        for end in range(start, n):
            substring = s[start:end + 1]
            if len(set(substring)) == len(substring):
                longest = max(longest, len(substring))
    return longest


def sliding_window(s: str) -> int:
    """
    Two pointers (left, right) define a window guaranteed to have no
    repeats. A hash map tracks the last index each character was seen at.
    When a repeat is found INSIDE the current window, left jumps directly
    past that repeat's previous position -- never re-scanning. O(n).
    """
    last_seen = {}
    left = 0
    longest = 0
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        longest = max(longest, right - left + 1)
    return longest


def test_longest_substring():
    cases = [
        ("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("", 0), ("a", 1),
        ("au", 2), ("dvdf", 3), ("abba", 2), ("tmmzuxt", 5),
    ]
    for s, expected in cases:
        bf, sw = substring_brute_force(s), sliding_window(s)
        assert bf == expected, f"brute_force({s!r}) = {bf}, expected {expected}"
        assert sw == expected, f"sliding_window({s!r}) = {sw}, expected {expected}"
    print(f"PASS: {len(cases)} correctness cases (Problem 1)")

    for trial in range(30):
        rng = random.Random(trial)
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 30)))
        assert substring_brute_force(s) == sliding_window(s), f"mismatch on {s!r}"
    print("PASS: 30 random cross-validation trials (Problem 1)")


# ===========================================================================
# Problem 2: Maximum Subarray Sum (Kadane's Algorithm)
# ===========================================================================

def subarray_brute_force(arr: list) -> int:
    """Check every contiguous subarray sum directly. O(n^2)."""
    if not arr:
        raise ValueError("array must be non-empty")
    n = len(arr)
    best = arr[0]
    for start in range(n):
        current_sum = 0
        for end in range(start, n):
            current_sum += arr[end]
            best = max(best, current_sum)
    return best


def kadane(arr: list) -> int:
    """
    One pass. best_ending_here = max(arr[i], best_ending_here + arr[i]).
    Track the max of best_ending_here seen so far. O(n).
    """
    if not arr:
        raise ValueError("array must be non-empty")
    best_ending_here = arr[0]
    best_overall = arr[0]
    for value in arr[1:]:
        best_ending_here = max(value, best_ending_here + value)
        best_overall = max(best_overall, best_ending_here)
    return best_overall


def test_max_subarray():
    cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6), ([1], 1), ([5, 4, -1, 7, 8], 23),
        ([-1], -1), ([-3, -2, -1], -1), ([0, 0, 0], 0), ([-1, -2, -3, -4], -1),
        ([2, -1, 2, 3, -9, 4], 6), ([1, 2, 3, 4, 5], 15),
    ]
    for arr, expected in cases:
        bf, kd = subarray_brute_force(arr), kadane(arr)
        assert bf == expected, f"brute_force({arr}) = {bf}, expected {expected}"
        assert kd == expected, f"kadane({arr}) = {kd}, expected {expected}"
    print(f"PASS: {len(cases)} correctness cases (Problem 2)")

    for trial in range(30):
        rng = random.Random(trial)
        arr = [rng.randint(-10, 10) for _ in range(rng.randint(1, 25))]
        assert subarray_brute_force(arr) == kadane(arr), f"mismatch on {arr}"

    # All-negative arrays specifically: a common bug initializes best=0,
    # which silently breaks this case since the correct answer must itself
    # be negative. Random data rarely happens to be all-negative on its own.
    for trial in range(10):
        rng = random.Random(trial + 1000)
        arr = [rng.randint(-10, -1) for _ in range(rng.randint(1, 15))]
        assert subarray_brute_force(arr) == kadane(arr), f"all-negative mismatch on {arr}"

    print("PASS: 30 random + 10 all-negative cross-validation trials (Problem 2)")


# ===========================================================================
# Benchmark
# ===========================================================================

def time_it(func, *args, trials: int = 3) -> float:
    best = float("inf")
    for _ in range(trials):
        start = time.perf_counter()
        func(*args)
        best = min(best, time.perf_counter() - start)
    return best


def run_benchmark():
    print("\nProblem 1: Longest Substring -- brute force O(n^3) vs sliding window O(n)")
    print(f"{'n':>8} | {'brute force (s)':>16} | {'sliding window (s)':>19}")
    print("-" * 50)
    rng = random.Random(1)
    for n in [50, 100, 150, 200, 300]:
        s = "".join(rng.choice("abcdefghij") for _ in range(n))
        bf_t = time_it(substring_brute_force, s)
        sw_t = time_it(sliding_window, s)
        print(f"{n:>8} | {bf_t:>16.4f} | {sw_t:>19.6f}")

    print("\nProblem 2: Max Subarray -- brute force O(n^2) vs Kadane's O(n)")
    print(f"{'n':>8} | {'brute force (s)':>16} | {'kadane (s)':>12}")
    print("-" * 42)
    rng = random.Random(2)
    for n in [500, 1_000, 2_000, 4_000, 8_000]:
        arr = [rng.randint(-100, 100) for _ in range(n)]
        bf_t = time_it(subarray_brute_force, arr)
        kd_t = time_it(kadane, arr)
        print(f"{n:>8} | {bf_t:>16.4f} | {kd_t:>12.6f}")

    print(
        "\nBoth optimized solutions share the same idea: carry forward exactly\n"
        "the information needed instead of recomputing it. Sliding window carries\n"
        "'what's in the current window' in a hash map instead of re-verifying\n"
        "substrings. Kadane's carries 'best sum ending here' instead of re-summing\n"
        "subarrays. The removed n^2/n^3 factor IS the redundant recomputation."
    )


if __name__ == "__main__":
    test_longest_substring()
    test_max_subarray()
    run_benchmark()
