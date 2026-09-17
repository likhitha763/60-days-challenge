#!/usr/bin/env python3
"""
================================================================================
MAXIMUM AVERAGE SUBARRAY - Fixed-Size Sliding Window
================================================================================

Problem (LeetCode 643 style):
  Given an integer array nums of length n and an integer k,
  find the contiguous subarray of length k that has the maximum average value.
  Return that maximum average.

Real-world use: gaming energy spikes, streaming analytics, financial monitoring,
real-time dashboards, sensor data analysis.

Approach:
  1. Naive   : O(n * k)  - compute sum of every window from scratch
  2. Optimized Sliding Window : O(n) - maintain a running sum, slide by
     subtracting the element leaving the window and adding the new one.

This file contains:
  - Clear explanations
  - Both implementations
  - Performance comparison
  - Simple ASCII visualization of the sliding window
  - Example run
================================================================================
"""

from typing import List
import time
import random


# ---------------------------------------------------------------------------
# 1. NAIVE SOLUTION  (O(n * k))
# ---------------------------------------------------------------------------
def max_average_naive(nums: List[int], k: int) -> float:
    """
    Brute-force: for every possible starting index i,
    compute the sum of nums[i : i+k] and keep the maximum average.
    Time  : O(n * k)
    Space : O(1)
    """
    n = len(nums)
    if n < k or k <= 0:
        raise ValueError("Invalid input: need n >= k > 0")

    max_avg = float("-inf")

    for i in range(n - k + 1):
        window_sum = sum(nums[i : i + k])          # O(k) work each time
        avg = window_sum / k
        if avg > max_avg:
            max_avg = avg

    return max_avg


# ---------------------------------------------------------------------------
# 2. OPTIMIZED SLIDING WINDOW  (O(n))
# ---------------------------------------------------------------------------
def max_average_sliding(nums: List[int], k: int) -> float:
    """
    Fixed-size sliding window:
      - Compute sum of the first window.
      - Then slide: subtract the outgoing element, add the incoming one.
      - Track the maximum sum (average = sum / k).
    Time  : O(n)
    Space : O(1)
    """
    n = len(nums)
    if n < k or k <= 0:
        raise ValueError("Invalid input: need n >= k > 0")

    # First window
    window_sum = sum(nums[:k])
    max_sum = window_sum

    # Slide the window
    for i in range(k, n):
        # Remove the element that is leaving (nums[i-k])
        # Add the new element that is entering (nums[i])
        window_sum += nums[i] - nums[i - k]
        if window_sum > max_sum:
            max_sum = window_sum

    return max_sum / k


# ---------------------------------------------------------------------------
# 3. VISUALIZATION OF WINDOW MOVEMENT
# ---------------------------------------------------------------------------
def visualize_sliding_window(nums: List[int], k: int) -> None:
    """
    Print a simple ASCII visualization showing how the fixed window
    moves across the array and which window produces the max average.
    """
    n = len(nums)
    if n < k:
        print("Cannot visualize: array shorter than window.")
        return

    print("\n" + "=" * 60)
    print("SLIDING WINDOW VISUALIZATION")
    print("=" * 60)
    print(f"Array : {nums}")
    print(f"k     : {k}")
    print("-" * 60)

    max_avg = float("-inf")
    best_start = 0
    window_sum = sum(nums[:k])

    def draw_step(start: int, current_sum: float, is_best: bool = False) -> None:
        avg = current_sum / k
        markers = []
        for i in range(n):
            if start <= i < start + k:
                markers.append(f"[{nums[i]:3d}]")
            else:
                markers.append(f" {nums[i]:3d} ")
        line = " ".join(markers)
        flag = "  <-- MAX" if is_best else ""
        print(f"start={start:2d}  sum={current_sum:6.1f}  avg={avg:7.3f}{flag}")
        print(f"         {line}")
        print()

    # First window
    draw_step(0, window_sum)
    max_avg = window_sum / k
    best_start = 0

    # Subsequent windows
    for i in range(k, n):
        window_sum += nums[i] - nums[i - k]
        start = i - k + 1
        avg = window_sum / k
        if avg > max_avg:
            max_avg = avg
            best_start = start
        draw_step(start, window_sum)

    print("-" * 60)
    print(f"Maximum average found: {max_avg:.5f}")
    print(f"Best window starts at index {best_start}: {nums[best_start:best_start+k]}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# 4. PERFORMANCE COMPARISON
# ---------------------------------------------------------------------------
def compare_performance(nums: List[int], k: int, repeats: int = 1000) -> None:
    """
    Time both approaches on the same input and print a simple comparison.
    """
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON (naive vs sliding window)")
    print("=" * 60)
    print(f"Array length n = {len(nums)}, window size k = {k}, repeats = {repeats}")

    # Warm-up
    _ = max_average_naive(nums, k)
    _ = max_average_sliding(nums, k)

    # Naive
    t0 = time.perf_counter()
    for _ in range(repeats):
        res_naive = max_average_naive(nums, k)
    t_naive = time.perf_counter() - t0

    # Sliding
    t0 = time.perf_counter()
    for _ in range(repeats):
        res_slide = max_average_sliding(nums, k)
    t_slide = time.perf_counter() - t0

    print(f"Naive result          : {res_naive:.6f}")
    print(f"Sliding window result : {res_slide:.6f}")
    print(f"Results match         : {abs(res_naive - res_slide) < 1e-9}")
    print()
    print(f"Naive total time      : {t_naive*1000:.2f} ms")
    print(f"Sliding total time    : {t_slide*1000:.2f} ms")
    if t_slide > 0:
        speedup = t_naive / t_slide
        print(f"Speedup (naive / slide) : {speedup:.1f}x")
    print("=" * 60)


# ---------------------------------------------------------------------------
# 5. MAIN - DEMO
# ---------------------------------------------------------------------------
def main() -> None:
    # Classic example
    nums = [1, 12, -5, -6, 50, 3]
    k = 4

    print("INPUT")
    print(f"  nums = {nums}")
    print(f"  k    = {k}")
    print()

    # Results
    avg_naive = max_average_naive(nums, k)
    avg_slide = max_average_sliding(nums, k)

    print("RESULTS")
    print(f"  Naive            → {avg_naive:.5f}")
    print(f"  Sliding Window   → {avg_slide:.5f}")
    print()

    # Visualization
    visualize_sliding_window(nums, k)

    # Performance on a larger array
    random.seed(42)
    large_nums = [random.randint(-100, 100) for _ in range(5000)]
    large_k = 100
    compare_performance(large_nums, large_k, repeats=50)

    print("\nDone. Key takeaway:")
    print("  Fixed-size sliding window turns O(n*k) into O(n)")
    print("  by reusing the previous window sum.")


if __name__ == "__main__":
    main()
