import math

from day28 import (
    two_sum_bruteforce,
    two_sum_optimized,
    compare_two_sum_algorithms,
    explain_lookup,
)


def test_two_sum_bruteforce_basic_case():
    nums = [2, 7, 11, 15]
    target = 9
    assert two_sum_bruteforce(nums, target) == [0, 1]


def test_two_sum_bruteforce_no_solution():
    nums = [1, 2, 3]
    target = 10
    assert two_sum_bruteforce(nums, target) is None


def test_two_sum_optimized_basic_case():
    nums = [3, 2, 4]
    target = 6
    assert two_sum_optimized(nums, target) == [1, 2]


def test_two_sum_optimized_duplicate_values():
    nums = [2, 2, 2]
    target = 4
    assert two_sum_optimized(nums, target) == [0, 1]


def test_compare_two_sum_algorithms_returns_metrics():
    result = compare_two_sum_algorithms([1, 5, 7, 11, 13], 18, trials=5)
    assert set(result.keys()) == {"bruteforce", "optimized"}
    assert result["bruteforce"]["duration_seconds"] >= 0
    assert result["optimized"]["duration_seconds"] >= 0
    assert result["bruteforce"]["indices"] == [0, 2]
    assert result["optimized"]["indices"] == [0, 2]


def test_explain_lookup_uses_hash_map_steps():
    steps = explain_lookup([2, 7, 11, 15], 9)
    assert isinstance(steps, list)
    assert any("complement" in step.lower() or "lookup" in step.lower() for step in steps)
    assert len(steps) >= 2


def test_two_sum_optimized_handles_empty_input():
    assert two_sum_optimized([], 0) is None
    assert two_sum_bruteforce([], 0) is None
