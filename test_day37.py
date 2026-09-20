"""Unit tests for the Day 37 Assign Cookies challenge."""

from day37 import assign_cookies


def test_assigns_smallest_sufficient_cookies():
    assert assign_cookies([1, 2, 3], [1, 1]) == 1


def test_skips_cookies_that_are_too_small():
    assert assign_cookies([1, 2], [1, 2, 3]) == 2


def test_exact_cookie_sizes_can_satisfy_children():
    assert assign_cookies([2, 3, 4], [2, 3, 4]) == 3


def test_handles_empty_inputs():
    assert assign_cookies([], [1, 2]) == 0
    assert assign_cookies([1, 2], []) == 0


def test_does_not_modify_inputs_while_sorting():
    greed_factors = [3, 1, 2]
    cookie_sizes = [2, 1, 3]

    assert assign_cookies(greed_factors, cookie_sizes) == 3
    assert greed_factors == [3, 1, 2]
    assert cookie_sizes == [2, 1, 3]