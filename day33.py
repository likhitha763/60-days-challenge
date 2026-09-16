"""Find the first defective robot version with binary search."""

from __future__ import annotations

from typing import Callable


def first_bad_version(
	version_count: int, is_bad_version: Callable[[int], bool]
) -> int:
	"""Return the first bad version from versions 1 through ``version_count``.

	The API is assumed to be monotonic: once a version is bad, every later
	version is also bad. The callback is evaluated at most
	``ceil(log2(version_count))`` times for a valid input.

	Raises:
		ValueError: If ``version_count`` is less than 1.

	The caller must provide a callback for which at least one version is bad.
	"""
	if version_count < 1:
		raise ValueError("version_count must be at least 1")

	left = 1
	right = version_count

	while left < right:
		middle = left + (right - left) // 2
		if is_bad_version(middle):
			right = middle
		else:
			left = middle + 1

	return left


def run_demo() -> None:
	"""Demonstrate the factory's version check."""
	bad_version = 37
	checks = 0

	def is_bad_version(version: int) -> bool:
		nonlocal checks
		checks += 1
		return version >= bad_version

	result = first_bad_version(100, is_bad_version)
	print(f"First bad version: {result}")
	print(f"API checks used: {checks}")


if __name__ == "__main__":
	run_demo()