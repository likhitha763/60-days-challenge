"""Greedy solution for the Assign Cookies problem.

Each child has a minimum cookie size they need for happiness. The greedy
strategy sorts both lists, then considers the least demanding child first.
The smallest cookie that can satisfy that child is used; smaller cookies are
skipped because they cannot satisfy anyone who needs at least as much.

This choice is safe because using a larger cookie for the current child could
only make fewer resources available to the remaining children. Repeating the
choice maximizes the number of satisfied children.
"""

from collections.abc import Sequence


def assign_cookies(
	greed_factors: Sequence[int], cookie_sizes: Sequence[int]
) -> int:
	"""Return the maximum number of children who can be made happy.

	A child with greed factor ``g`` is satisfied by a cookie of size ``s``
	when ``s >= g``. The input sequences are not modified.

	Time complexity is O(n log n + m log m), where n and m are the numbers of
	children and cookies. The sorted copies use O(n + m) additional space.
	"""
	sorted_greed = sorted(greed_factors)
	sorted_cookies = sorted(cookie_sizes)
	child_index = 0

	for cookie_size in sorted_cookies:
		if child_index == len(sorted_greed):
			break
		if cookie_size >= sorted_greed[child_index]:
			child_index += 1

	return child_index


def run_demo() -> None:
	"""Show the greedy assignment on a festival example."""
	greed_factors = [1, 2, 3]
	cookie_sizes = [1, 1]
	happy_children = assign_cookies(greed_factors, cookie_sizes)

	print("=== Festival Cookie Distribution ===")
	print(f"Child requirements: {greed_factors}")
	print(f"Cookie sizes: {cookie_sizes}")
	print(f"Maximum happy children: {happy_children}")


if __name__ == "__main__":
	run_demo()
