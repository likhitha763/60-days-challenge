"""
Digital Kingdom Archive Validator (Validate Binary Search Tree)
==============================================================
Phase: Tree Validation

Description:
A digital kingdom archive stores historical records using Binary Search Trees (BST). 
Unfortunately, data corruption has broken the structure of some records. This script 
validates whether the kingdom records still strictly adhere to BST rules.

Real-World Impact:
- Databases: Ensuring index tree integrity for fast lookups.
- Distributed Architectures: Validating range partitions across nodes.
- File Systems: Verifying hierarchical directory metadata consistency.
"""

class TreeNode:
    """Definition for a binary tree node representing a record in the archive."""
    def __init__(self, val: int = 0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst_recursive(root: TreeNode | None, min_val: float = float('-inf'), max_val: float = float('inf')) -> bool:
    """
    Approach 1: Recursive DFS with Range Tracking (Optimal)
    -------------------------------------------------------
    Every node must fall within a specific valid range (min_val < node.val < max_val).
    When moving left, the current node's value becomes the upper bound.
    When moving right, the current node's value becomes the lower bound.
    
    Time Complexity: O(N) where N is the number of records.
    Space Complexity: O(H) where H is the height of the tree (recursion stack).
    """
    if not root:
        return True
        
    # The current node's value must strictly lie between min_val and max_val
    if not (min_val < root.val < max_val):
        return False
        
    # Recursively validate left and right subtrees with updated bounds
    return (is_valid_bst_recursive(root.left, min_val, root.val) and 
            is_valid_bst_recursive(root.right, root.val, max_val))


def is_valid_bst_inorder(root: TreeNode | None) -> bool:
    """
    Approach 2: In-Order Traversal Check
    ------------------------------------
    An in-order traversal (Left, Root, Right) of a valid BST must produce 
    a strictly increasing sequence of values.
    
    Time Complexity: O(N)
    Space Complexity: O(H)
    """
    stack = []
    current = root
    prev_val = float('-inf')
    
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
            
        current = stack.pop()
        
        # If the current value is less than or equal to the previous, it's not a BST
        if current.val <= prev_val:
            return False
            
        prev_val = current.val
        current = current.right
        
    return True


def visualize_bst_validation(root: TreeNode | None, min_val=float('-inf'), max_val=float('inf'), level=0) -> bool:
    """
    Visualizer: Traces how boundary ranges narrow down during validation.
    """
    indent = "  " * level
    if not root:
        print(f"{indent}-> [Empty branch (Valid)]")
        return True
        
    print(f"{indent}-> Checking Record ID {root.val} | Valid Range: ({min_val} < x < {max_val})")
    
    if not (min_val < root.val < max_val):
        print(f"{indent}*** CORRUPTION DETECTED: Value {root.val} violates range ({min_val}, {max_val})! ***")
        return False
        
    print(f"{indent}   Valid! Inspecting left subtree (max bound updates to {root.val})...")
    left_valid = visualize_bst_validation(root.left, min_val, root.val, level + 1)
    
    if not left_valid:
        return False
        
    print(f"{indent}   Valid! Inspecting right subtree (min bound updates to {root.val})...")
    right_valid = visualize_bst_validation(root.right, root.val, max_val, level + 1)
    
    return right_valid


# --- Execution and Testing ---
if __name__ == "__main__":
    print("=== DIGITAL KINGDOM ARCHIVE VALIDATION SYSTEM ===")
    
    # Test Case 1: Valid Kingdom Archive BST
    #          [Record 2]
    #         /          \
    #    [Record 1]    [Record 3]
    valid_archive = TreeNode(2, TreeNode(1), TreeNode(3))
    
    print("\n[Test 1: Valid Archive BST]")
    print(f"Recursive Range Validation : {is_valid_bst_recursive(valid_archive)}")
    print(f"In-Order Sequence Check    : {is_valid_bst_inorder(valid_archive)}")
    
    print("\n--- Visualizing Valid Tree Traversal ---")
    visualize_bst_validation(valid_archive)
    
    print("\n" + "="*50)
    
    # Test Case 2: Corrupted/Invalid Archive BST (Subtree violation)
    #          [Record 5]
    #         /          \
    #    [Record 1]    [Record 4]
    #                  /        \
    #             [Record 3]  [Record 6]
    # Note: 3 is on the right of 5, but 3 < 5! This makes it an invalid BST.
    corrupted_archive = TreeNode(
        5, 
        TreeNode(1), 
        TreeNode(4, TreeNode(3), TreeNode(6))
    )
    
    print("\n[Test 2: Corrupted/Invalid Archive BST]")
    print(f"Recursive Range Validation : {is_valid_bst_recursive(corrupted_archive)}")
    print(f"In-Order Sequence Check    : {is_valid_bst_inorder(corrupted_archive)}")
    
    print("\n--- Visualizing Corrupted Tree Traversal ---")
    visualize_bst_validation(corrupted_archive)
