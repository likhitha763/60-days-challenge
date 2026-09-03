"""Reverse Polish Notation evaluator for the Robot Calculator Arena.

RPN places each operator after its operands. The evaluator uses a stack:
numbers are pushed, and an operator pops the right and left operands, applies
the operation, then pushes the result back.
"""

from collections.abc import Sequence


def _divide_toward_zero(left: int, right: int) -> int:
	"""Divide integers with the truncation rule used by the arena."""
	quotient = abs(left) // abs(right)
	return -quotient if (left < 0) != (right < 0) else quotient


def evaluate_rpn(expression: str | Sequence[str]) -> int:
	"""Evaluate an RPN expression and return its integer result.

	``expression`` may be a whitespace-delimited string or a sequence of
	tokens, for example ``"2 1 + 3 *"`` or ``["2", "1", "+", "3", "*"]``.
	Supported operators are ``+``, ``-``, ``*``, and ``/``. Division truncates
	toward zero, matching common calculator and programming-language rules.
	"""
	tokens = expression.split() if isinstance(expression, str) else expression
	stack: list[int] = []
	operators = {"+", "-", "*", "/"}

	for token in tokens:
		if token not in operators:
			try:
				stack.append(int(token))
			except (TypeError, ValueError) as error:
				raise ValueError(f"Invalid RPN token: {token!r}") from error
			continue

		if len(stack) < 2:
			raise ValueError(f"Operator {token!r} is missing an operand")

		right = stack.pop()
		left = stack.pop()

		if token == "+":
			result = left + right
		elif token == "-":
			result = left - right
		elif token == "*":
			result = left * right
		else:
			if right == 0:
				raise ZeroDivisionError("RPN expression attempted division by zero")
			result = _divide_toward_zero(left, right)

		stack.append(result)

	if len(stack) != 1:
		raise ValueError("RPN expression must leave exactly one result")

	return stack[0]


if __name__ == "__main__":
	attacks = [
		"2 1 + 3 *",  # (2 + 1) * 3 = 9
		["4", "13", "5", "/", "+"],  # 4 + (13 / 5) = 6
		["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],
	]

	for attack in attacks:
		print(f"{attack} = {evaluate_rpn(attack)}")
