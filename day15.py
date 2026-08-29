"""
Tests (stdlib only). Run with: python tests/test_detector.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from detector import has_duplicates_bruteforce, has_duplicates_set, find_duplicate_ids_set


def test_no_duplicates():
    ids = ["A1", "A2", "A3", "A4"]
    assert has_duplicates_bruteforce(ids) is False
    assert has_duplicates_set(ids) is False
    print("PASS: test_no_duplicates")


def test_with_duplicate():
    ids = ["A1", "A2", "A3", "A2"]
    assert has_duplicates_bruteforce(ids) is True
    assert has_duplicates_set(ids) is True
    print("PASS: test_with_duplicate")


def test_empty_list():
    assert has_duplicates_bruteforce([]) is False
    assert has_duplicates_set([]) is False
    print("PASS: test_empty_list")


def test_single_element():
    assert has_duplicates_bruteforce(["A1"]) is False
    assert has_duplicates_set(["A1"]) is False
    print("PASS: test_single_element")


def test_duplicate_at_boundaries():
    ids = ["A1", "A2", "A3", "A1"]  # first and last identical
    assert has_duplicates_bruteforce(ids) is True
    assert has_duplicates_set(ids) is True
    print("PASS: test_duplicate_at_boundaries")


def test_find_duplicate_ids_set_returns_correct_set():
    ids = ["A1", "A2", "A2", "A3", "A1", "A4"]
    dupes = find_duplicate_ids_set(ids)
    assert dupes == {"A1", "A2"}, f"got {dupes}"
    print("PASS: test_find_duplicate_ids_set_returns_correct_set")


def test_both_implementations_agree_on_random_data():
    import random
    random.seed(42)
    for _ in range(20):
        size = random.randint(0, 50)
        pool_size = random.randint(1, max(1, size))
        ids = [f"AGENT-{random.randint(0, pool_size)}" for _ in range(size)]
        bf = has_duplicates_bruteforce(ids)
        st = has_duplicates_set(ids)
        assert bf == st, f"mismatch on {ids}: brute={bf} set={st}"
    print("PASS: test_both_implementations_agree_on_random_data")


if __name__ == "__main__":
    test_no_duplicates()
    test_with_duplicate()
    test_empty_list()
    test_single_element()
    test_duplicate_at_boundaries()
    test_find_duplicate_ids_set_returns_correct_set()
    test_both_implementations_agree_on_random_data()
    print("\nAll tests passed.")