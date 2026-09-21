"""Unit tests for the Day 38 binary tree traversal challenge."""

from day38 import (
    BinaryTreeNode,
    build_royal_tree,
    compare_traversals,
    inorder_iterative,
    inorder_recursive,
    visualize_inorder,
)


def test_recursive_and_iterative_traversals_match_on_royal_tree():
    root = build_royal_tree()

    expected = [1, 3, 6, 8, 10, 14]
    assert inorder_recursive(root) == expected
    assert inorder_iterative(root) == expected


def test_traversals_handle_empty_and_single_node_trees():
    assert inorder_recursive(None) == []
    assert inorder_iterative(None) == []
    assert inorder_recursive(BinaryTreeNode(42)) == [42]
    assert inorder_iterative(BinaryTreeNode(42)) == [42]


def test_traversals_handle_a_right_skewed_tree():
    root = BinaryTreeNode(1, right=BinaryTreeNode(2, right=BinaryTreeNode(3)))

    assert inorder_recursive(root) == [1, 2, 3]
    assert inorder_iterative(root) == [1, 2, 3]


def test_visualization_includes_order_and_agreement():
    diagram = visualize_inorder(build_royal_tree())

    assert "Binary tree:" in diagram
    assert "Inorder (left -> root -> right): [1, 3, 6, 8, 10, 14]" in diagram
    assert "Recursive == iterative: True" in diagram


def test_comparison_reports_matching_values_and_timings():
    result = compare_traversals(build_royal_tree())

    assert result["same_result"] is True
    assert result["recursive"]["values"] == result["iterative"]["values"]
    assert result["recursive"]["seconds"] >= 0
    assert result["iterative"]["seconds"] >= 0
