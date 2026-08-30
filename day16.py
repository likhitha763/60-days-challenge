"""Recursive staircase problem.

A robot can climb either 1 or 2 steps at a time. This script shows:
1. a direct recursive solution,
2. a memoized optimization,
3. a quick comparison of execution time for both approaches.

The number of ways to reach step n follows:
ways(0) = 1
ways(1) = 1
ways(n) = ways(n - 1) + ways(n - 2)
"""

from __future__ import annotations

import time
from functools import lru_cache


def count_ways_recursive(n: int) -> int:
    """Brute-force recursive solution.

    Time complexity: O(2^n)
    Space complexity: O(n) recursion stack
    """
    if n < 0:
        return 0
    if n == 0:
        return 1
    return count_ways_recursive(n - 1) + count_ways_recursive(n - 2)


@lru_cache(maxsize=None)
def count_ways_memoized(n: int) -> int:
    """Memoized dynamic programming version.

    Time complexity: O(n)
    Space complexity: O(n)
    """
    if n < 0:
        return 0
    if n == 0:
        return 1
    return count_ways_memoized(n - 1) + count_ways_memoized(n - 2)


def explain_recursion_tree(n: int) -> None:
    """Print a compact explanation of the recursion tree."""
    print(f"\nRecursion tree for n = {n}")
    print("Each call branches into (n-1) and (n-2), creating overlapping subproblems.")
    print("For example, for n = 4:")
    print("      ways(4)")
    print("     /       \\")
    print(" ways(3)   ways(2)")
    print(" /   \\    /   \\")
    print("w2   w1   w1   w0")
    print("The same smaller values are recomputed many times in the recursive version.")


def compare_execution_times(target: int = 35) -> None:
    """Compare naive recursive vs memoized execution time."""
    start = time.perf_counter()
    recursive_result = count_ways_recursive(target)
    recursive_time = time.perf_counter() - start

    start = time.perf_counter()
    memoized_result = count_ways_memoized(target)
    memoized_time = time.perf_counter() - start

    print(f"\nTarget step count: {target}")
    print(f"Recursive result: {recursive_result}")
    print(f"Memoized result: {memoized_result}")
    print(f"Recursive time: {recursive_time:.6f} seconds")
    print(f"Memoized time: {memoized_time:.6f} seconds")
    print(f"Speedup: {recursive_time / memoized_time:.2f}x")


def main() -> None:
    print("Robot staircase counting problem")
    print("A robot can climb 1 or 2 steps at a time.")

    n = 10
    print(f"\nNumber of ways to reach step {n}: {count_ways_recursive(n)}")
    print(f"Optimized memoized answer: {count_ways_memoized(n)}")

    explain_recursion_tree(4)
    compare_execution_times(35)


if __name__ == "__main__":
    main()
