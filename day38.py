"""Binary tree inorder traversal with recursive and iterative solutions.

Inorder traversal visits each node in the order left subtree, root, right
subtree. For a binary search tree, that visit order produces sorted values.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter


@dataclass
class BinaryTreeNode:
	"""A node in a binary tree."""

	value: int
	left: BinaryTreeNode | None = None
	right: BinaryTreeNode | None = None


def inorder_recursive(root: BinaryTreeNode | None) -> list[int]:
	"""Return node values using recursive left-root-right traversal."""
	values: list[int] = []

	def visit(node: BinaryTreeNode | None) -> None:
		if node is None:
			return
		visit(node.left)
		values.append(node.value)
		visit(node.right)

	visit(root)
	return values


def inorder_iterative(root: BinaryTreeNode | None) -> list[int]:
	"""Return node values using an explicit stack instead of call recursion."""
	values: list[int] = []
	stack: list[BinaryTreeNode] = []
	current = root

	while current is not None or stack:
		while current is not None:
			stack.append(current)
			current = current.left

		current = stack.pop()
		values.append(current.value)
		current = current.right

	return values


def visualize_inorder(root: BinaryTreeNode | None) -> str:
	"""Return a compact diagram showing the tree and its inorder sequence."""
	recursive_values = inorder_recursive(root)
	iterative_values = inorder_iterative(root)

	if root is None:
		tree_diagram = "(empty tree)"
	else:
		tree_diagram = (
			f"        {root.value}\n"
			f"       /  \\\n"
			f"      {root.left.value if root.left else '-'}    "
			f"{root.right.value if root.right else '-'}"
		)

	return (
		"Binary tree:\n"
		f"{tree_diagram}\n\n"
		"Inorder (left -> root -> right): "
		f"{recursive_values}\n"
		f"Recursive == iterative: {recursive_values == iterative_values}"
	)


def compare_traversals(root: BinaryTreeNode | None) -> dict[str, object]:
	"""Compare results and elapsed time for both traversal approaches."""
	start = perf_counter()
	recursive_values = inorder_recursive(root)
	recursive_seconds = perf_counter() - start

	start = perf_counter()
	iterative_values = inorder_iterative(root)
	iterative_seconds = perf_counter() - start

	return {
		"recursive": {"values": recursive_values, "seconds": recursive_seconds},
		"iterative": {"values": iterative_values, "seconds": iterative_seconds},
		"same_result": recursive_values == iterative_values,
	}


def build_royal_tree() -> BinaryTreeNode:
	"""Build the sample royal lineage used by the runnable demonstration."""
	return BinaryTreeNode(
		8,
		left=BinaryTreeNode(3, BinaryTreeNode(1), BinaryTreeNode(6)),
		right=BinaryTreeNode(10, None, BinaryTreeNode(14)),
	)


def run_demo() -> None:
	"""Display the sample tree, traversal order, and timing comparison."""
	royal_tree = build_royal_tree()
	print(visualize_inorder(royal_tree))
	print("\nComparison:")
	print(compare_traversals(royal_tree))


if __name__ == "__main__":
	run_demo()
