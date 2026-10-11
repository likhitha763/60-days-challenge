"""Focused tests for the Day 58 mock interview solutions."""

from day58 import (
    binary_search,
    broken_binary_search,
    longest_unique_substring_length,
)


def test_longest_unique_substring_examples_and_boundaries():
    assert longest_unique_substring_length("abcabcbb") == 3
    assert longest_unique_substring_length("bbbbb") == 1
    assert longest_unique_substring_length("pwwkew") == 3
    assert longest_unique_substring_length("") == 0


def test_longest_unique_substring_does_not_move_window_backwards():
    assert longest_unique_substring_length("abba") == 2


def test_binary_search_finds_boundaries_and_reports_missing_values():
    values = [2, 4, 7, 9]

    assert binary_search(values, 2) == 0
    assert binary_search(values, 9) == 3
    assert binary_search(values, 5) == -1
    assert binary_search([], 5) == -1


def test_broken_binary_search_exposes_final_element_bug():
    assert broken_binary_search([2, 4, 7, 9], 9) == -1