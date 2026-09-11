"""
Pattern Recognition: Two Sum Treasure Map
=======================================

A pirate captain hid a treasure clue as a target sum.
Given a list of coordinate values, find two indices whose values
combine to the target treasure number.

This file includes:
1. A brute-force solution
2. An optimized hash-map solution
3. Runtime comparison between both approaches
4. A visual explanation of the lookup process

Real-world impact:
- financial transaction matching
- recommendation systems
- search optimization and indexing
"""

from __future__ import annotations

import time
from typing import List, Optional, Dict, Any


def two_sum_bruteforce(nums: List[int], target: int) -> Optional[List[int]]:
    """Return the first pair of indices whose values add to target.

    This is the straightforward approach: test every pair of positions.
    Time complexity: O(n^2)
    Space complexity: O(1)
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return None


def two_sum_optimized(nums: List[int], target: int) -> Optional[List[int]]:
    """Return the pair indices using a hash map.

    Store each seen number with its index. For each current number,
    check whether its complement has already been seen.
    Time complexity: O(n)
    Space complexity: O(n)
    """
    seen: Dict[int, int] = {}

    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index

    return None


def compare_two_sum_algorithms(nums: List[int], target: int, trials: int = 1000) -> Dict[str, Dict[str, Any]]:
    """Compare brute-force and optimized runtimes."""
    results: Dict[str, Dict[str, Any]] = {}

    for name, solver in {
        "bruteforce": two_sum_bruteforce,
        "optimized": two_sum_optimized,
    }.items():
        start = time.perf_counter()
        for _ in range(trials):
            result = solver(nums, target)
        elapsed = time.perf_counter() - start
        results[name] = {
            "duration_seconds": elapsed,
            "indices": result,
        }

    return results


def explain_lookup(nums: List[int], target: int) -> List[str]:
    """Return a readable trace of how the hash map finds the answer."""
    seen: Dict[int, int] = {}
    steps: List[str] = []

    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            steps.append(
                f"Index {index}: value={value}, complement={complement}. "
                f"Found {complement} at index {seen[complement]}, so the treasure pair is "
                f"({seen[complement]}, {index})."
            )
            return steps

        seen[value] = index
        steps.append(
            f"Index {index}: value={value}, looking for {complement}. "
            f"Stored {value} in the lookup table at index {index}."
        )

    steps.append("No valid pair exists for this target.")
    return steps


def visualize_lookup(nums: List[int], target: int) -> str:
    """Return an ASCII visualization of the lookup process."""
    seen: Dict[int, int] = {}
    lines: List[str] = ["LOOKUP TABLE VISUALIZATION", "=" * 28]

    for index, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            lines.append(
                f"Step {index}: {value} + {complement} = {target} -> found pair "
                f"(index {seen[complement]}, index {index})"
            )
            lines.append(f"Table: {seen}")
            break

        seen[value] = index
        lines.append(f"Step {index}: store {value} at index {index} -> lookup so far: {seen}")
        lines.append(f"Need complement: {complement}")
    else:
        lines.append("No treasure pair found.")

    return "\n".join(lines)


def run_demo() -> None:
    """Demonstrate the pirate treasure map challenge."""
    treasure_map = [2, 7, 11, 15]
    target = 9

    print("=== Pirate Treasure Map: Two Sum ===")
    print(f"Coordinates: {treasure_map}")
    print(f"Target treasure sum: {target}")
    print()

    brute_force = two_sum_bruteforce(treasure_map, target)
    optimized = two_sum_optimized(treasure_map, target)

    print(f"Brute-force answer: {brute_force}")
    print(f"Optimized answer:   {optimized}")
    print()

    print("Lookup trace:")
    for step in explain_lookup(treasure_map, target):
        print(" -", step)
    print()

    print(visualize_lookup(treasure_map, target))
    print()

    stats = compare_two_sum_algorithms(treasure_map, target, trials=20000)
    print("Runtime comparison (20,000 trials):")
    for name, info in stats.items():
        print(f" - {name}: {info['duration_seconds']:.8f} seconds -> {info['indices']}")


if __name__ == "__main__":
    run_demo()
