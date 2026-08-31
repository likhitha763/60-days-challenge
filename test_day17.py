"""Unit tests for Day 17: Treasure Chest Combination Generator."""

try:
    import pytest
except ImportError:
    pytest = None

from day17_Treasure_Chest_Combination_Generator import (
    generate_gem_combinations,
    count_combinations
)


def test_empty_gems():
    gems = []
    result = generate_gem_combinations(gems)
    assert result == [[]]
    assert len(result) == 1
    assert count_combinations(gems) == 1


def test_single_gem():
    gems = ["Ruby"]
    result = generate_gem_combinations(gems)
    assert len(result) == 2
    assert [] in result
    assert ["Ruby"] in result
    assert count_combinations(gems) == 2


def test_three_gems_subsets():
    gems = ["Ruby", "Emerald", "Sapphire"]
    result = generate_gem_combinations(gems)
    
    # 2^3 = 8 combinations
    assert len(result) == 8
    assert count_combinations(gems) == 8
    
    # Verify all expected subsets exist regardless of order
    expected = [
        [],
        ["Ruby"],
        ["Emerald"],
        ["Sapphire"],
        ["Emerald", "Ruby"],
        ["Emerald", "Sapphire"],
        ["Ruby", "Sapphire"],
        ["Emerald", "Ruby", "Sapphire"]
    ]
    
    # Convert inner lists to tuples for set comparison
    result_set = {tuple(sorted(res)) for res in result}
    expected_set = {tuple(sorted(exp)) for exp in expected}
    assert result_set == expected_set


def test_four_gems():
    gems = ["Ruby", "Emerald", "Sapphire", "Diamond"]
    result = generate_gem_combinations(gems)
    assert len(result) == 16
    assert count_combinations(gems) == 16


def test_duplicates_handling():
    gems = ["Diamond", "Ruby", "Diamond"]
    result_deduped = generate_gem_combinations(gems, handle_duplicates=True)
    result_with_dups = generate_gem_combinations(gems, handle_duplicates=False)
    
    # Without dedup: 2^3 = 8
    assert len(result_with_dups) == 8
    
    # With dedup: Unique subsets are [], [Diamond], [Diamond, Diamond], [Diamond, Diamond, Ruby], [Diamond, Ruby], [Ruby] -> 6
    assert len(result_deduped) == 6


if __name__ == "__main__":
    test_empty_gems()
    test_single_gem()
    test_three_gems_subsets()
    test_four_gems()
    test_duplicates_handling()
    print("All Day 17 combination tests passed successfully!")
