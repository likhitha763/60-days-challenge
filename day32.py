"""Binary search for fast lookups in sorted data.

Binary search repeatedly discards the half of the search space that cannot
contain the target. The module also includes a linear-search baseline,
readable search-space visualization, and a runtime comparison helper.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Sequence


def linear_search(values: Sequence[int], target: int) -> int:
	"""Return the first index of target using a one-by-one scan.

	Returns -1 when target is absent. Time complexity is O(n).
	"""
	for index, value in enumerate(values):
		if value == target:
			return index
	return -1


def binary_search(values: Sequence[int], target: int) -> int:
	"""Return the index of target in sorted values using iteration.

	Returns -1 when target is absent. Time complexity is O(log n), with
	O(1) additional space.
	"""
	left = 0
	right = len(values) - 1

	while left <= right:
		middle = left + (right - left) // 2
		if values[middle] == target:
			return middle
		if values[middle] < target:
			left = middle + 1
		else:
			right = middle - 1

	return -1


def visualize_binary_search(values: Sequence[int], target: int) -> str:
	"""Return an ASCII trace showing the search range shrinking."""
	left = 0
	right = len(values) - 1
	lines = ["BINARY SEARCH VISUALIZATION", "=" * 28]
	step = 1

	while left <= right:
		middle = left + (right - left) // 2
		lines.append(
			f"Step {step}: range [{left}, {right}], middle={middle}, "
			f"value={values[middle]}"
		)
		if values[middle] == target:
			lines.append(f"Found {target} at index {middle}.")
			return "\n".join(lines)
		if values[middle] < target:
			lines.append("Target is larger; discard the left half.")
			left = middle + 1
		else:
			lines.append("Target is smaller; discard the right half.")
			right = middle - 1
		step += 1

	lines.append(f"{target} is not in the sorted data.")
	return "\n".join(lines)


def compare_search_algorithms(
	values: Sequence[int], target: int, trials: int = 1000
) -> Dict[str, Dict[str, Any]]:
	"""Compare linear and binary search runtimes and returned indices."""
	if trials < 1:
		raise ValueError("trials must be at least 1")

	results: Dict[str, Dict[str, Any]] = {}
	algorithms: Dict[str, Callable[[Sequence[int], int], int]] = {
		"linear": linear_search,
		"binary": binary_search,
	}

	for name, search in algorithms.items():
		start = time.perf_counter()
		result = -1
		for _ in range(trials):
			result = search(values, target)
		elapsed = time.perf_counter() - start
		results[name] = {
			"duration_seconds": elapsed,
			"index": result,
		}

	return results


def run_demo() -> None:
	"""Demonstrate the vault search and its performance difference."""
	vault_codes = list(range(0, 1_000_000, 2))
	target = 876_542

	print("=== Secret Vault: Binary Search ===")
	print(f"Vault contains {len(vault_codes):,} sorted codes.")
	print(f"Target code: {target}")
	print()
	print(visualize_binary_search(vault_codes, target))
	print()

	results = compare_search_algorithms(vault_codes, target, trials=50)
	print("Runtime comparison (50 trials):")
	for name, info in results.items():
		print(
			f" - {name}: {info['duration_seconds']:.8f} seconds "
			f"-> index {info['index']}"
		)


if __name__ == "__main__":
	run_demo()
