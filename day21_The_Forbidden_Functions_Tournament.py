"""
Week 3 Sprint Challenge: Recursion + Stack, No Built-in Helpers
=================================================================
Constraint: sort(), sum(), max(), min() are NOT used anywhere below.
Every operation they would normally provide is built by hand instead.

Problem 1 (Recursion): compute sum, max, and min of a list recursively.
Problem 2 (Stack):     validate balanced brackets using a manual stack.

Run this file directly to see the tests execute and the reflection print.
"""


# ---------------------------------------------------------------------------
# Problem 1: Recursion — sum, max, min without sum()/max()/min()
# ---------------------------------------------------------------------------

def recursive_stats(numbers: list, index: int = 0) -> dict:
    """
    Recursively compute (sum, max, min) of `numbers` in a single traversal.

    Base case: index == len(numbers) - 1 (last element) -> that element is
    the running sum/max/min so far.
    Recursive case: combine the current element with the result of
    processing the rest of the list.

    Returns a dict: {"sum": ..., "max": ..., "min": ...}
    Raises ValueError on an empty list (max/min are undefined for empty input).
    """
    if len(numbers) == 0:
        raise ValueError("recursive_stats: cannot compute stats of an empty list")

    if index == len(numbers) - 1:
        value = numbers[index]
        return {"sum": value, "max": value, "min": value}

    rest = recursive_stats(numbers, index + 1)
    current = numbers[index]

    # Manual max: compare, don't call max()
    running_max = current if current > rest["max"] else rest["max"]
    # Manual min: compare, don't call min()
    running_min = current if current < rest["min"] else rest["min"]
    # Manual sum: add, don't call sum()
    running_sum = current + rest["sum"]

    return {"sum": running_sum, "max": running_max, "min": running_min}


# ---------------------------------------------------------------------------
# Problem 2: Stack — balanced brackets validator
# ---------------------------------------------------------------------------

def is_balanced(expression: str) -> bool:
    """
    Check whether all brackets in `expression` are balanced and correctly
    nested: (), [], {} in any combination.

    Uses a plain list as a manual stack: append() = push, pop() = pop.
    No collections.deque, no regex, no sort/sum/max/min.
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    openers = set(pairs.values())
    closers = set(pairs.keys())

    stack = []  # manual stack

    for char in expression:
        if char in openers:
            stack.append(char)  # push
        elif char in closers:
            if len(stack) == 0:
                return False  # closing bracket with nothing open
            top = stack.pop()  # pop
            if top != pairs[char]:
                return False  # mismatched pair, e.g. "(]"
        # any other character is ignored (not part of this problem's scope)

    return len(stack) == 0  # balanced only if every opener was closed


# ---------------------------------------------------------------------------
# Tests (assert-based, no external test framework)
# ---------------------------------------------------------------------------

def run_tests():
    # --- recursive_stats ---
    r = recursive_stats([3, 7, 1, 9, 4])
    assert r == {"sum": 24, "max": 9, "min": 1}, r

    r = recursive_stats([5])
    assert r == {"sum": 5, "max": 5, "min": 5}, r

    r = recursive_stats([-3, -1, -7, -2])
    assert r == {"sum": -13, "max": -1, "min": -7}, r

    r = recursive_stats([4, 4, 4])
    assert r == {"sum": 12, "max": 4, "min": 4}, r

    try:
        recursive_stats([])
        assert False, "expected ValueError on empty list"
    except ValueError:
        pass

    print("PASS: recursive_stats (5 cases)")

    # --- is_balanced ---
    assert is_balanced("()") is True
    assert is_balanced("()[]{}") is True
    assert is_balanced("{[()]}") is True
    assert is_balanced("(]") is False
    assert is_balanced("([)]") is False
    assert is_balanced("(((") is False
    assert is_balanced(")") is False
    assert is_balanced("") is True
    assert is_balanced("a(b[c]d)e") is True  # non-bracket chars ignored
    assert is_balanced("(a]") is False

    print("PASS: is_balanced (10 cases)")


# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------

REFLECTION = """
Reflection: What "no built-in helpers" actually forces you to think about
--------------------------------------------------------------------------
Banning sum()/max()/min() doesn't make the logic harder to understand --
it makes it harder to hide. sum() collapses "add these up" into one call
you never have to look at again. Writing it recursively means every add
is visible, and it becomes obvious that the base case and the combine
step are the only two real decisions in the whole function -- everything
else is bookkeeping.

The stack problem was less about the ban (list.append/pop were always
fine here) and more about noticing that "check if brackets are balanced"
is actually two decisions per character, not one: does this token open
or close something, and if it closes something, does it close the RIGHT
thing. It's easy to write a version that checks "does it close something"
and skip the "right thing" check -- that's exactly what makes "([)]"
tricky: it fails on nesting order, not on bracket count. A stack makes
the check natural because it's the same order the brackets nested in.

Net effect of the constraint: it doesn't make me a better debugger by
teaching me to write helper functions from scratch (I will use max()
in real code tomorrow and that's correct, not lazy). It's useful because
it forces you to notice which part of a "solved" problem you'd otherwise
never look at -- and that's usually where the edge cases live.
"""


if __name__ == "__main__":
    run_tests()
    print(REFLECTION)
