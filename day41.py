"""
Lowest Common Ancestor (LCA) of a Binary Search Tree
=====================================================

Real-world angle: "find the closest common ancestor" is the same query used
by file systems (closest common directory of two files), network routing
(closest common router on two paths), org charts (closest common manager of
two employees), and version control (git merge-base finds the closest
common commit ancestor).

This file is self-contained:
  1. Builds a BST from a list of values.
  2. Finds the LCA of two node values using BST-specific properties.
  3. Prints the decision made at every node visited (left / right / stop).
  4. Renders a PNG visualizing the tree with the search path highlighted.

Run:
    python lca_bst.py
Output:
    Console trace of the traversal + lca_visualization.png in the same folder.
"""

from __future__ import annotations
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# 1. BST construction
# ---------------------------------------------------------------------------
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: "TreeNode | None" = None
        self.right: "TreeNode | None" = None


def insert(root: "TreeNode | None", val: int) -> TreeNode:
    """Standard BST insert. Duplicate values are silently ignored."""
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root


def build_bst(values: list[int]) -> TreeNode:
    root = None
    for v in values:
        root = insert(root, v)
    return root


# ---------------------------------------------------------------------------
# 2. Lowest Common Ancestor
# ---------------------------------------------------------------------------
def lowest_common_ancestor(root: TreeNode, p: int, q: int, verbose: bool = True):
    """
    Find the LCA of the nodes holding values p and q in a BST.

    Why this works (the BST property is what makes this fast):
      - If both p and q are smaller than the current node's value, the LCA
        must live in the left subtree -- neither target can be reached by
        going right, so there's no reason to search there.
      - If both are larger, the LCA must live in the right subtree, for the
        same reason mirrored.
      - The first node where p and q are no longer on the same side (one is
        <= the node and the other is >=) is the exact point where the two
        search paths diverge. That node is the LCA -- it's the deepest
        node that is still an ancestor of both.

    This gives an O(h) iterative solution (h = tree height), O(1) extra
    space. Contrast with a *general* binary tree, where the BST ordering
    property doesn't hold: there, you'd have to recursively search both
    subtrees for p and q separately (or build root-to-node paths and diff
    them), which costs O(n) since every node might need to be visited.

    Returns:
        (lca_node, path_values) -- path_values is the list of node values
        visited on the way to the LCA, in order (useful for the diagram).
    """
    node = root
    path = []
    while node:
        path.append(node.val)
        if p < node.val and q < node.val:
            if verbose:
                print(f"  At {node.val}: {p} and {q} are both smaller -> go LEFT")
            node = node.left
        elif p > node.val and q > node.val:
            if verbose:
                print(f"  At {node.val}: {p} and {q} are both larger -> go RIGHT")
            node = node.right
        else:
            if verbose:
                print(f"  At {node.val}: paths split here -> LCA is {node.val}")
            return node, path
    return None, path  # p or q not present as a straddling pair in this tree


# ---------------------------------------------------------------------------
# 3. Visualization
# ---------------------------------------------------------------------------
def _assign_positions(node, depth, counter, positions):
    """In-order x-position + depth-based y-position, so the drawing reads
    left-to-right the same way the BST's values are ordered."""
    if node is None:
        return
    _assign_positions(node.left, depth + 1, counter, positions)
    x = counter[0]
    counter[0] += 1
    positions[node.val] = (x, -depth)
    _assign_positions(node.right, depth + 1, counter, positions)


def visualize(root: TreeNode, path: list[int], p: int, q: int,
              lca_val: int, out_path: str = "lca_visualization.png"):
    positions = {}
    _assign_positions(root, 0, [0], positions)

    fig, ax = plt.subplots(figsize=(10, 6))

    def draw_edges(node):
        if node is None:
            return
        x0, y0 = positions[node.val]
        for child in (node.left, node.right):
            if child is not None:
                x1, y1 = positions[child.val]
                ax.plot([x0, x1], [y0, y1], color="#B0B0B0", zorder=1, linewidth=1.5)
                draw_edges(child)

    draw_edges(root)

    for val, (x, y) in positions.items():
        if val == lca_val:
            face, edge, txt = "#2E7D32", "#1B5E20", "white"   # LCA: green
        elif val in (p, q):
            face, edge, txt = "#1565C0", "#0D47A1", "white"   # targets: blue
        elif val in path:
            face, edge, txt = "#FFB300", "#E65100", "black"   # visited on the way: amber
        else:
            face, edge, txt = "#EDEDED", "#9E9E9E", "black"   # untouched node: grey
        ax.scatter([x], [y], s=1100, color=face, edgecolors=edge,
                   linewidths=2, zorder=2)
        ax.text(x, y, str(val), ha="center", va="center",
                color=txt, fontsize=11, fontweight="bold", zorder=3)

    ax.scatter([], [], s=200, color="#2E7D32", label=f"LCA ({lca_val})")
    ax.scatter([], [], s=200, color="#1565C0", label=f"Targets ({p}, {q})")
    ax.scatter([], [], s=200, color="#FFB300", label="Visited on search path")
    ax.scatter([], [], s=200, color="#EDEDED", label="Not visited")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=4, frameon=False)

    ax.set_title(f"LCA search for {p} and {q}  ->  LCA = {lca_val}", fontsize=13)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"\nVisualization saved to: {out_path}")


# ---------------------------------------------------------------------------
# 4. Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    values = [20, 10, 30, 5, 15, 25, 35, 3, 7, 12, 18]
    root = build_bst(values)

    p, q = 3, 15

    print(f"Finding LCA of {p} and {q}")
    print("Traversal decisions:")
    lca_node, path = lowest_common_ancestor(root, p, q)

    if lca_node:
        print(f"\nResult: LCA({p}, {q}) = {lca_node.val}")
        visualize(root, path, p, q, lca_node.val)
    else:
        print("One or both values were not found on a single straddling path.")
