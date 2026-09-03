"""Unit tests for the Day 20 Robot Calculator Arena."""

import pytest

from day20_Robot_Calculator_Arena import evaluate_rpn


def test_evaluates_string_with_multiple_operators():
    assert evaluate_rpn("2 1 + 3 *") == 9


def test_accepts_token_sequence():
    assert evaluate_rpn(["4", "13", "5", "/", "+"]) == 6


def test_handles_negative_values_and_division_toward_zero():
    assert evaluate_rpn(["7", "-3", "/"]) == -2
    assert evaluate_rpn(["-7", "3", "/"]) == -2


def test_handles_long_expression():
    expression = "10 6 9 3 + -11 * / * 17 + 5 +"
    assert evaluate_rpn(expression) == 22


def test_rejects_invalid_expression_shapes():
    with pytest.raises(ValueError, match="missing an operand"):
        evaluate_rpn("2 +")

    with pytest.raises(ValueError, match="exactly one result"):
        evaluate_rpn("2 3")

    with pytest.raises(ValueError, match="Invalid RPN token"):
        evaluate_rpn("2 nope +")


def test_rejects_division_by_zero():
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        evaluate_rpn("8 0 /")