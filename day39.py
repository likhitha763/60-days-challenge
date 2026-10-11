"""
Dungeon Depth Analyzer (Maximum Depth of Binary Tree)
=====================================================
Phase: Tree Depth Analysis

Description:
A game engine generates massive underground dungeons structured as binary trees. 
This script calculates the maximum possible depth of the dungeon before players 
get trapped, comparing multiple DFS and BFS approaches, handling edge cases 
gracefully, and visualizing recursive traversal.

Real-World Impact:
- AI Search Systems: Evaluating game trees and minimax lookahead limits.
- Recursive Analysis: Traversing nested directory structures or component hierarchies.
- Infrastructure Monitoring: Tracing hierarchical cloud network layers.
"""

from collections import deque

class TreeNode:
    """Definition for a binary tree node representing a dungeon chamber."""
    def __init__(self, val: int = 0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth_recursive(root: TreeNode | None) -> int:
    """
    Approach 1: Recursive Depth-First Search (DFS)
    ------------------------------------------------
    Elegantly calculates the depth by asking sub-chambers for their maximum 
    depth and adding 1 for the current chamber.
    
    Time Complexity: O(N) where N is the total number of chambers.
    Space Complexity: O(H) where H is the height of the dungeon tree (call stack).
    """
    if not root:
        return 0
    left_depth = max_depth_recursive(root.left)
    right_depth = max_depth_recursive(root.right)
    return 1 + max(left_depth, right_depth)


def max_depth_iterative_dfs(root: TreeNode | None) -> int:
    """
    Approach 2: Iterative Depth-First Search (DFS) using a Stack
    -----------------------------------------------------------
    Avoids recursion limit issues in extremely deep dungeons by managing 
    an explicit stack holding nodes and their current depth.
    
    Time Complexity: O(N)
    Space Complexity: O(H)
    """
    if not root:
        return 0
        
    stack = [(root, 1)]
    max_depth = 0
    
    while stack:
        node, depth = stack.pop()
        if node:
            max_depth = max(max_depth, depth)
            # Push right and left children with incremented depth
            if node.right:
                stack.append((node.right, depth + 1))
            if node.left:
                stack.append((node.left, depth + 1))
                
    return max_depth


def max_depth_bfs(root: TreeNode | None) -> int:
    """
    Approach 3: Breadth-First Search (Level Order Traversal)
    -------------------------------------------------------
    Traverses the dungeon level by level, incrementing the depth counter 
    for each complete tier explored.
    
    Time Complexity: O(N)
    Space Complexity: O(W) where W is the maximum width of the tree.
    """
    if not root:
        return 0
        
    queue = deque([root])
    depth = 0
    
    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        depth += 1
        
    return depth


def visualize_dungeon_traversal(root: TreeNode | None) -> int:
    """
    Visualizer: Traces recursive depth calculation step-by-step
    to show how the game engine evaluates chamber layers.
    """
    print("\n--- Visualizing Recursive Dungeon Traversal ---")
    
    def trace(node, level=0):
        indent = "  " * level
        if not node:
            print(f"{indent}-> [Dead End / Empty Chamber (Depth: 0)]")
            return 0
        print(f"{indent}-> Exploring Chamber {node.val} (Level: {level + 1})")
        left_depth = trace(node.left, level + 1)
        right_depth = trace(node.right, level + 1)
        current_max = 1 + max(left_depth, right_depth)
        print(f"{indent}<- Leaving Chamber {node.val} | Max depth from here: {current_max}")
        return current_max

    return trace(root)


# --- Execution and Testing ---
if __name__ == "__main__":
    print("=== DUNGEON DEPTH ANALYSIS SYSTEM ===")
    
    # Test Case 1: Standard Balanced Dungeon Tree
    #          [Chamber 1]
    #         /           \
    #    [Chamber 2]    [Chamber 3]
    #    /         \
    # [Chamber 4] [Chamber 5]
    root1 = TreeNode(1, 
                TreeNode(2, TreeNode(4), TreeNode(5)), 
                TreeNode(3)
            )
    
    print("\n[Test 1: Standard Balanced Dungeon]")
    print(f"Recursive DFS Depth : {max_depth_recursive(root1)}")
    print(f"Iterative DFS Depth : {max_depth_iterative_dfs(root1)}")
    print(f"BFS Level-Order Depth: {max_depth_bfs(root1)}")
    
    # Run visualization for Test 1
    visualize_dungeon_traversal(root1)
    
    print("\n" + "="*50)
    
    # Test Case 2: Edge Case - Empty Dungeon (None)
    root2 = None
    print("\n[Test 2: Edge Case - Empty Dungeon]")
    print(f"Depth: {max_depth_recursive(root2)}")
    
    # Test Case 3: Edge Case - Skewed Dungeon (Linear Linked List structure)
    # [1] -> [2] -> [3] (All right children)
    root3 = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    print("\n[Test 3: Edge Case - Skewed Linear Dungeon]")
    print(f"Depth: {max_depth_iterative_dfs(root3)}")
