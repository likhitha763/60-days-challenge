"""Unit tests for the Day 32 Binary Search challenge."""

import pytest

from day32 import (
    binary_search,
    compare_search_algorithms,
    linear_search,
    visualize_binary_search,
)


def test_binary_search_finds_target_in_sorted_values():
    assert binary_search([3, 8, 14, 21, 35], 21) == 3


def test_binary_search_returns_minus_one_when_target_is_missing():
    assert binary_search([3, 8, 14, 21, 35], 10) == -1


def test_searches_handle_empty_values():
    assert binary_search([], 10) == -1
    assert linear_search([], 10) == -1


def test_visualization_shows_ranges_shrinking_and_result():
    trace = visualize_binary_search([2, 4, 6, 8, 10, 12, 14], 12)
    assert "range [0, 6]" in trace
    assert "discard" in trace
    assert "Found 12 at index 5" in trace


def test_visualization_reports_missing_target():
    assert "is not in the sorted data" in visualize_binary_search([1, 3, 5], 4)


def test_comparison_returns_matching_results_and_timings():
    result = compare_search_algorithms(list(range(0, 100, 2)), 42, trials=5)
    assert set(result) == {"linear", "binary"}
    assert result["linear"]["index"] == 21
    assert result["binary"]["index"] == 21
    assert result["linear"]["duration_seconds"] >= 0
    assert result["binary"]["duration_seconds"] >= 0


def test_comparison_rejects_zero_trials():
    with pytest.raises(ValueError, match="at least 1"):
        compare_search_algorithms([1, 2, 3], 2, trials=0)