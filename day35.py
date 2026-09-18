#!/usr/bin/env python3
"""
================================================================================
DAY 35 – LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS
Advanced Variable-Size Sliding Window
================================================================================

Problem (LeetCode 3):
  Given a string s, find the length of the longest substring without repeating
  characters.

Real-World Impact:
  - Cybersecurity: detecting unique signal patterns before corruption/repetition
  - Network analysis: unique session tokens / packet sequences
  - Compression systems & NLP pipelines

Approach:
  Variable-size sliding window with a hash map tracking the last seen index
  of each character.
  - Expand the right pointer freely
  - When a duplicate is found, shrink the left pointer past the previous
    occurrence of that character
  - Track the maximum window length seen

Time  : O(n)  – each character is visited at most twice
Space : O(min(n, alphabet)) – the hash map size is bounded by unique chars

This file contains:
  - Optimized O(n) implementation
  - Character last-seen tracking
  - Clear expansion & shrinking logic
  - ASCII visualization of left/right pointer movement
  - Example runs
================================================================================
"""

from typing import Dict


def length_of_longest_substring(s: str) -> int:
    """
    Optimized variable sliding window.
    Returns the length of the longest substring without repeating characters.
    """
    n = len(s)
    if n == 0:
        return 0

    last_seen: Dict[str, int] = {}   # char -> most recent index
    left = 0
    max_len = 0

    for right in range(n):
        char = s[right]

        # If the character was seen and is still inside the current window,
        # shrink the window by moving left past the previous occurrence.
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        # Update the most recent index of the current character
        last_seen[char] = right

        # Window size = right - left + 1
        max_len = max(max_len, right - left + 1)

    return max_len


def length_of_longest_substring_with_trace(s: str) -> int:
    """
    Same algorithm but prints a step-by-step visualization of the
    left and right pointers as the window expands and shrinks.
    """
    n = len(s)
    if n == 0:
        print("Empty string → length 0")
        return 0

    last_seen: Dict[str, int] = {}
    left = 0
    max_len = 0
    best_window = ""

    print("=" * 70)
    print(f'INPUT STRING: "{s}"')
    print("=" * 70)
    print(f"{'Step':<6} {'Left':<6} {'Right':<6} {'Char':<6} {'Window':<20} {'Len':<5} Action")
    print("-" * 70)

    for right in range(n):
        char = s[right]
        action = "expand"

        if char in last_seen and last_seen[char] >= left:
            # Shrink
            old_left = left
            left = last_seen[char] + 1
            action = f"shrink (left {old_left}→{left})"

        last_seen[char] = right
        current_len = right - left + 1
        window = s[left:right + 1]

        if current_len > max_len:
            max_len = current_len
            best_window = window

        print(f"{right:<6} {left:<6} {right:<6} {char:<6} {window:<20} {current_len:<5} {action}")

    print("-" * 70)
    print(f'Longest substring without repeats: "{best_window}" (length {max_len})')
    print("=" * 70)
    return max_len


def visualize_pointers(s: str) -> None:
    """
    Compact ASCII view showing left/right pointers.
    """
    n = len(s)
    last_seen: Dict[str, int] = {}
    left = 0
    max_len = 0

    print("\nPointer movement (L = left, R = right, B = both):")
    print("-" * 50)

    for right in range(n):
        char = s[right]
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)

        # Build visual line
        line = list(" " * n)
        for i in range(left, right + 1):
            line[i] = s[i]
        markers = [" "] * n
        markers[left] = "L"
        markers[right] = "R"
        if left == right:
            markers[left] = "B"  # both

        print(f"step {right:2d}: {''.join(line)}")
        print(f"         {''.join(markers)}")

    print("-" * 50)
    print(f"Max length found: {max_len}")


# ---------------------------------------------------------------------------
# Demo / Test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        "abcabcbb",      # expected 3 ("abc")
        "bbbbb",         # expected 1 ("b")
        "pwwkew",        # expected 3 ("wke")
        "dvdf",          # expected 3 ("vdf")
        "",              # expected 0
        "a",             # expected 1
        "au",            # expected 2
        "aab",           # expected 2 ("ab")
        "tmmzuxt",       # expected 5 ("mzuxt")
    ]

    print("\n=== CORRECTNESS CHECKS ===\n")
    for s in test_cases:
        result = length_of_longest_substring(s)
        print(f'  "{s}" → {result}')

    print("\n\n=== DETAILED TRACE (example: 'abcabcbb') ===\n")
    length_of_longest_substring_with_trace("abcabcbb")

    print("\n\n=== POINTER VISUALIZATION (example: 'pwwkew') ===")
    visualize_pointers("pwwkew")

    print("\nDone.")
