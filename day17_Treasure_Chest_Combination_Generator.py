"""Day 17: Treasure Chest Combination Generator (Backtracking & Search)

This module solves the magical treasure chest problem by generating all possible
gem combinations (subsets / power set) that a player can carry using Backtracking.

Real-World Impact:
    Backtracking is a general algorithm for finding all (or some) solutions to computational
    problems by incrementally building candidates and abandoning ("backtracking") a candidate
    as soon as it determines the candidate cannot lead to a valid solution.
    It powers scheduling systems, recommendation engines, AI decision trees, constraint satisfaction
    solvers (e.g., Sudoku, N-Queens), and combinatorial routing algorithms.

Key Concepts:
    - Power Set: A set of all possible subsets (size = 2^N for N unique items).
    - Backtracking paradigm: State Space Tree search with Choice -> Explore -> Backtrack (Undo).
"""

from __future__ import annotations
import sys
from typing import List, Any


def generate_gem_combinations(gems: List[str], handle_duplicates: bool = True) -> List[List[str]]:
    """Generate all possible gem combinations (subsets) using Backtracking.

    Args:
        gems: List of gem names available in the treasure chest.
        handle_duplicates: If True, eliminates duplicate subset outputs when input contains identical gems.

    Returns:
        List of all combinations (subsets), where each combination is a list of gem names.

    Time Complexity: O(N * 2^N) where N is the number of gems.
    Space Complexity: O(N) auxiliary stack memory for recursion depth.
    """
    results: List[List[str]] = []
    
    # If handling duplicates, sort the list so identical gems are adjacent
    working_gems = sorted(gems) if handle_duplicates else list(gems)
    
    def backtrack(index: int, current_bag: List[str]) -> None:
        # Base case: every state in the decision tree represents a valid subset
        results.append(list(current_bag))
        
        for i in range(index, len(working_gems)):
            # Skip duplicates at the same tree depth if requested
            if handle_duplicates and i > index and working_gems[i] == working_gems[i - 1]:
                continue
                
            # 1. CHOOSE: Add gem to current bag
            current_bag.append(working_gems[i])
            
            # 2. EXPLORE: Recursively generate combinations starting from the next index
            backtrack(i + 1, current_bag)
            
            # 3. BACKTRACK (UNDO): Remove the gem to explore paths without this gem
            current_bag.pop()

    backtrack(0, [])
    return results


def count_combinations(gems: List[str], unique_only: bool = True) -> int:
    """Calculate the expected total combinations count.
    
    For N unique items, total combinations = 2^N (including empty combination).
    """
    if unique_only:
        unique_gems = set(gems)
        return 1 << len(unique_gems)  # 2^N
    return 1 << len(gems)


def format_decision_tree(gems: List[str]) -> str:
    """Generate an ASCII visual representation of the decision tree for include/exclude choices."""
    lines = [
        f"Decision Tree for Gems: {gems}",
        "=" * 50,
        "Root: [] (Empty bag)"
    ]
    
    def build_tree_str(index: int, current_path: List[str], prefix: str = "", is_last: bool = True) -> None:
        if index == len(gems):
            return
        
        gem = gems[index]
        connector = "\\-- " if is_last else "+-- "
        
        # Choice 1: Include
        inc_path = current_path + [gem]
        lines.append(f"{prefix}{connector}INCLUDE '{gem}' -> {inc_path}")
        new_prefix = prefix + ("    " if is_last else "|   ")
        build_tree_str(index + 1, inc_path, new_prefix, False)
        
        # Choice 2: Exclude
        exc_connector = "\\-- "
        lines.append(f"{prefix}{exc_connector}EXCLUDE '{gem}' -> {current_path}")
        build_tree_str(index + 1, current_path, new_prefix, True)

    build_tree_str(0, [])
    return "\n".join(lines)


def print_backtracking_explanation() -> None:
    """Print detailed explanation of the Backtracking mechanism."""
    explanation = """
================================================================================
                    HOW BACKTRACKING WORKS (3 STEPS)
================================================================================
1. CHOOSE (Make a decision):
   - At each decision point (gem index i), decide whether to pick or skip the gem.
   - Append the gem to the player's current bag.

2. EXPLORE (Recursive Depth-First Search):
   - Recursively call the solver for the remaining items (index + 1).
   - This moves deeper down the decision tree toward a leaf node.

3. BACKTRACK / UNDO (Revert the decision):
   - Remove the last gem from the bag (`current_bag.pop()`).
   - Restores the state so the program can explore alternative paths (e.g. skipping the gem).

Why Backtracking is Efficient:
   - State space tree search builds paths incrementally.
   - It avoids allocating new lists at every recursion step by mutating and restoring a single shared array.
   - Can prune invalid paths early (e.g., if total capacity or weight limit is exceeded).
================================================================================
"""
    print(explanation)


def display_combinations_demo(gems: List[str]) -> None:
    """Run a complete demonstration for a given set of gems."""
    print(f"\n[GEMS] Treasure Chest Gems Input: {gems}")
    combinations = generate_gem_combinations(gems)
    
    print(f"Total Combinations Generated: {len(combinations)}")
    print(f"Theoretical Formula (2^N): {count_combinations(gems)}")
    print("\nAll Possible Combinations:")
    for idx, combo in enumerate(combinations, 1):
        formatted_combo = ", ".join(combo) if combo else "Empty Bag"
        print(f"  Combo #{idx:02d}: [{formatted_combo}]")


def main() -> None:
    print("=================================================================")
    print("   DAY 17: TREASURE CHEST COMBINATION GENERATOR (BACKTRACKING)   ")
    print("=================================================================")
    
    # 1. Backtracking Mechanism Explanation
    print_backtracking_explanation()
    
    # 2. Main Example with 3 Gems
    sample_gems = ["Ruby", "Emerald", "Sapphire"]
    display_combinations_demo(sample_gems)
    
    # 3. Visualizing Decision Tree
    print("\n" + "=" * 50)
    print("DECISION TREE VISUALIZATION")
    print("=" * 50)
    print(format_decision_tree(sample_gems))
    
    # 4. Special Case: Duplicates
    duplicate_gems = ["Diamond", "Ruby", "Diamond"]
    print("\n" + "=" * 50)
    print("SPECIAL CASE: GEMS WITH DUPLICATES")
    print("=" * 50)
    display_combinations_demo(duplicate_gems)


if __name__ == "__main__":
    main()
