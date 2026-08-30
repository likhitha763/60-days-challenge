from day16 import count_ways_recursive, count_ways_memoized


def test_small_cases():
    assert count_ways_recursive(0) == 1
    assert count_ways_recursive(1) == 1
    assert count_ways_recursive(2) == 2
    assert count_ways_recursive(3) == 3
    assert count_ways_recursive(4) == 5

    assert count_ways_memoized(0) == 1
    assert count_ways_memoized(1) == 1
    assert count_ways_memoized(2) == 2
    assert count_ways_memoized(3) == 3
    assert count_ways_memoized(4) == 5


def test_matches_for_larger_values():
    for n in range(0, 15):
        assert count_ways_recursive(n) == count_ways_memoized(n)


if __name__ == "__main__":
    test_small_cases()
    test_matches_for_larger_values()
    print("All staircase tests passed.")
