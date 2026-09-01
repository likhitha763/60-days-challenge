"""
Ancient Message Bracket Validator — Stack

Problem: An ancient civilization stored messages using nested brackets.
Before a message can be decoded, verify that every bracket is properly
matched and correctly nested — supporting multiple bracket types: (),
[], and {}.

Approach: Stack (LIFO — Last In, First Out).

Why a stack specifically: when we see a closing bracket, it must match
the MOST RECENTLY opened bracket that hasn't been closed yet — not the
oldest one. That "most recent first" requirement is exactly what a
stack gives you for free. A queue (FIFO) would match closing brackets
against the OLDEST unclosed bracket instead, which is the wrong order
for nesting.

Time complexity:  O(n) — one pass through the message, O(1) work per character
Space complexity: O(n) — worst case, every character is an opening bracket
                   sitting on the stack (e.g. "((((((")
"""

from typing import Optional


# Maps each closing bracket to the opening bracket it must match
CLOSING_TO_OPENING = {
    ")": "(",
    "]": "[",
    "}": "{",
}
OPENING_BRACKETS = set(CLOSING_TO_OPENING.values())
CLOSING_BRACKETS = set(CLOSING_TO_OPENING.keys())


def is_balanced(message: str) -> bool:
    """
    Return True if every bracket in `message` is properly matched and
    nested. Non-bracket characters (letters, numbers, spaces, symbols)
    are part of the message's text and are simply ignored.
    """
    stack = []

    for char in message:
        if char in OPENING_BRACKETS:
            # Push: remember we're now "inside" this bracket, waiting
            # for its matching close.
            stack.append(char)

        elif char in CLOSING_BRACKETS:
            # A closing bracket must match whatever was opened MOST
            # RECENTLY — i.e. whatever is currently on top of the stack.
            if not stack:
                # Closing bracket with nothing open to match -> invalid
                return False

            most_recent_open = stack.pop()
            expected_open = CLOSING_TO_OPENING[char]
            if most_recent_open != expected_open:
                # Wrong type of bracket closed (e.g. "(" closed by "]")
                return False

        # else: not a bracket at all -> ignore, it's just message text

    # Valid only if every opened bracket found its match.
    # If the stack isn't empty, something was opened but never closed.
    return len(stack) == 0


def first_error_position(message: str) -> Optional[int]:
    """
    Like is_balanced, but returns the INDEX of the first problem
    character if the message is invalid, or None if it's balanced.
    Useful for pointing at exactly where decoding should stop.
    """
    stack = []  # each entry: (bracket_char, index)

    for i, char in enumerate(message):
        if char in OPENING_BRACKETS:
            stack.append((char, i))

        elif char in CLOSING_BRACKETS:
            if not stack:
                return i  # closing bracket with nothing open

            most_recent_open, _ = stack.pop()
            if most_recent_open != CLOSING_TO_OPENING[char]:
                return i  # mismatched bracket type

    if stack:
        # Something opened but never closed -> report the first
        # unclosed opening bracket's position.
        return stack[0][1]

    return None


if __name__ == "__main__":
    sample_messages = [
        "Hello (world [test])",
        "{[()]}",
        "(]",
        "(((",
        "The scroll reads: {ancient [wisdom (lives)]}",
    ]

    for msg in sample_messages:
        result = is_balanced(msg)
        status = "VALID — safe to decode" if result else "INVALID — do not decode"
        print(f"{status:26} | {msg}")
