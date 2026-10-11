"""
Dungeon Treasure Hunter Optimizer (House Robber)
==============================================
Phase: Dynamic Programming

Description:
A treasure hunter explores a dungeon filled with gold rooms. Because adjacent 
rooms are connected by trap alarms, robbing two adjacent rooms triggers an alarm. 
This script calculates the maximum amount of treasure that can be collected 
without triggering security systems.

Real-World Impact:
- Resource Planning: Allocating budgets where competing projects cannot overlap.
- Investment Systems: Selecting non-consecutive high-yield assets to maximize returns.
- Scheduling Engines: Maximizing task throughput with mutual exclusion constraints.
"""

def rob_optimized(nums: list[int]) -> int:
    """
    Approach 1: Bottom-Up Dynamic Programming with O(1) Space (Optimal)
    -------------------------------------------------------------------
    At any room `i`, the hunter has two choices:
    1. Skip the current room: Keep the max loot up to room `i-1`.
    2. Rob the current room: Add room `i`'s gold to the max loot up to room `i-2`.
    
    Recurrence Relation:
    dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    
    Time Complexity: O(N) where N is the number of rooms.
    Space Complexity: O(1) auxiliary space by only tracking the last two states.
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
        
    # Track max loot from two houses back (rob1) and one house back (rob2)
    rob1, rob2 = 0, 0
    
    for gold in nums:
        # Current max is either skipping this room (rob2) or taking it (rob1 + gold)
        current_max = max(rob2, rob1 + gold)
        rob1 = rob2
        rob2 = current_max
        
    return rob2


def why_greedy_fails_explanation() -> str:
    """
    Explains why a Greedy approach fails for this problem:
    ------------------------------------------------------
    If a greedy algorithm simply picks the room with the maximum gold at each step, 
    it might pick a massive treasure room and block itself from robbing two or three 
    subsequent rooms that cumulatively hold much more gold. 
    
    Dynamic Programming solves this by looking ahead via optimal substructure, 
    balancing immediate gains against future possibilities.
    """
    return (
        "Greedy algorithms make locally optimal choices that lead to globally suboptimal "
        "outcomes here. For example, in [2, 7, 9, 3, 1], a greedy picker might grab 9 first, "
        "blocking access to 7 and 3 (total 9). DP correctly evaluates combinations like "
        "2 + 9 + 1 = 12 or 7 + 3 = 10, finding the true maximum of 12."
    )


def visualize_decision_choices(nums: list[int]):
    """
    Visualizer: Traces the dynamic programming decision choices room by room,
    showing whether to rob or skip based on accumulated totals.
    """
    print("\n--- Visualizing Dungeon Room Decisions ---")
    if not nums:
        print("No rooms to explore.")
        return
        
    print(f"Room Gold Values: {nums}")
    print("Evaluating optimal choices step-by-step:")
    
    rob1, rob2 = 0, 0
    for i, gold in enumerate(nums):
        decision_skip = rob2
        decision_rob = rob1 + gold
        
        if decision_rob > decision_skip:
            action = f"ROB room {i} (Gain {gold} + prev stash {rob1} = {decision_rob})"
            new_rob2 = decision_rob
        else:
            action = f"SKIP room {i} (Keeping previous max stash {rob2})"
            new_rob2 = decision_skip
            
        rob1 = rob2
        rob2 = new_rob2
        print(f"Room {i} [Gold: {gold}] -> Decision: {action} | Running Max: {rob2}")
        
    print(f"-> Maximum safe treasure collected: {rob2}\n")


# --- Execution and Testing ---
if __name__ == "__main__":
    print("=== DUNGEON TREASURE HUNTER OPTIMIZER ===")
    
    # Test Case 1: Standard dungeon corridor
    dungeon_loot_1 = [1, 2, 3, 1]
    print(f"\n[Test 1: Room Gold {dungeon_loot_1}]")
    print(f"Maximum Safe Loot: {rob_optimized(dungeon_loot_1)}")
    visualize_decision_choices(dungeon_loot_1)
    
    print("=" * 50)
    
    # Test Case 2: Complex trap layout where greedy would fail
    dungeon_loot_2 = [2, 7, 9, 3, 1]
    print(f"\n[Test 2: Room Gold {dungeon_loot_2}]")
    print(f"Maximum Safe Loot: {rob_optimized(dungeon_loot_2)}")
    visualize_decision_choices(dungeon_loot_2)
    
    print("\n[Architecture Note]")
    print(why_greedy_fails_explanation())
