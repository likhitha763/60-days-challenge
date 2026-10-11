"""Day 58 mock interview arena: DSA, debugging, and system design."""


def longest_unique_substring_length(text: str) -> int:
	"""Return the longest substring length containing no repeated characters.

	Runs in O(n) time with O(min(n, alphabet_size)) auxiliary space.
	"""
	last_seen = {}
	window_start = 0
	longest = 0

	for index, character in enumerate(text):
		previous_index = last_seen.get(character, -1)
		if previous_index >= window_start:
			window_start = previous_index + 1

		last_seen[character] = index
		longest = max(longest, index - window_start + 1)

	return longest


def broken_binary_search(values: list[int], target: int) -> int:
	"""Broken interview snippet: misses a target at the final index."""
	left = 0
	right = len(values) - 1

	while left < right:
		middle = (left + right) // 2
		if values[middle] == target:
			return middle
		if values[middle] < target:
			left = middle + 1
		else:
			right = middle - 1

	return -1


def binary_search(values: list[int], target: int) -> int:
	"""Return the index of target in sorted values, or -1 if it is absent."""
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


def main() -> None:
	sample = "abcabcbb"
	print("DSA: longest unique substring")
	print(f"Input: {sample!r}; answer: {longest_unique_substring_length(sample)}")

	values = [2, 4, 7, 9]
	target = 9
	print("\nDebugging: binary search")
	print(f"Broken implementation returns: {broken_binary_search(values, target)}")
	print(f"Corrected implementation returns: {binary_search(values, target)}")

	print("\nSystem design: URL shortener")
	print("Request path: API -> key generation -> durable mapping store")
	print("Redirect path: cache -> mapping store -> HTTP 302 redirect")


if __name__ == "__main__":
	main()
