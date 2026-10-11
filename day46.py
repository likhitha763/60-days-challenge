"""
Rooftop Robot Battery Optimizer (Min Cost Climbing Stairs)
=========================================================
Phase: Dynamic Programming

Description:
A robot must travel across dangerous rooftops while conserving battery. Each jump 
drains energy based on the height/risk of the rooftop. This script calculates 
the minimum energy path to reach the top before the robot shuts down.

Real-World Impact:
- Robotics & Autonomous Vehicles: Energy-efficient path planning.
- Finance: Option pricing and multi-period portfolio optimization.
- AI Planning: Finding optimal action sequences in game trees and search spaces.
"""

def min_cost_climbing_stairs_bottom_up(cost: list[int]) -> int:
    """
    Approach 1: Bottom-Up DP with Space Optimization (Optimal)
    ---------------------------------------------------------
    Instead of using an array to store all states, we only track the last two 
    steps because the cost to reach step i only depends on i-1 and i-2.
    
    Time Complexity: O(N) where N is the number of steps.
    Space Complexity: O(1) auxiliary space.
    """
    n = len(cost)
    if n <= 1:
        return 0
        
    prev2 = cost[0] # Cost to reach step i-2
    prev1 = cost[1] # Cost to reach step i-1
    
    for i in range(2, n):
        current = cost[i] + min(prev1, prev2)
        prev2 = prev1
        prev1 = current
        
    # The top can be reached from either the last or second-to-last step
    return min(prev1, prev2)


def min_cost_climbing_stairs_memo(cost: list[int]) -> int:
    """
    Approach 2: Top-Down DP (Memoization)
    --------------------------------------
    Recursively breaks down the problem from the top, caching results of sub-problems
    to avoid redundant calculations (which plague pure exponential recursion).
    
    Time Complexity: O(N)
    Space Complexity: O(N) for recursion stack and memoization dictionary.
    """
    memo = {}
    
    def dp(i):
        if i < 2:
            return cost[i]
        if i in memo:
            return memo[i]
            
        memo[i] = cost[i] + min(dp(i - 1), dp(i - 2))
        return memo[i]
        
    n = len(cost)
    # The top is beyond the last index (index n), reachable from n-1 or n-2
    return min(dp(n - 1), dp(n - 2))


def visualize_state_transitions(cost: list[int]):
    """
    Visualizer: Traces how state costs accumulate step-by-step from the bottom up,
    comparing choices at each rooftop tier.
    """
    print("\n--- Visualizing Rooftop DP State Transitions ---")
    n = len(cost)
    if n == 0:
        return
        
    print(f"Rooftop Energy Costs: {cost}")
    print("Computing optimal cumulative energy at each step:")
    
    dp_table = [0] * n
    dp_table[0] = cost[0]
    if n > 1:
        dp_table[1] = cost[1]
        
    print(f"Step 0 -> Cost: {dp_table[0]}")
    if n > 1:
        print(f"Step 1 -> Cost: {dp_table[1]}")
        
    for i in range(2, n):
        chosen_prev = min(dp_table[i - 1], dp_table[i - 2])
        dp_table[i] = cost[i] + chosen_prev
        source = f"Step {i-1} ({dp_table[i-1]})" if dp_table[i-1] < dp_table[i-2] else f"Step {i-2} ({dp_table[i-2]})"
        print(f"Step {i} -> Cost {cost[i]} + min({source}) = Total Cumulative Cost: {dp_table[i]}")
        
    final_min = min(dp_table[-1], dp_table[-2])
    print(f"-> Minimum energy required to clear top: {final_min}\n")


# --- Execution and Testing ---
if __name__ == "__main__":
    print("=== ROOFTOP ROBOT BATTERY OPTIMIZER ===")
    
    # Test Case 1: Standard battery grid
    rooftop_costs_1 = [10, 15, 20]
    print(f"\n[Test 1: Costs {rooftop_costs_1}]")
    print(f"Bottom-Up Optimized Cost : {min_cost_climbing_stairs_bottom_up(rooftop_costs_1)}")
    print(f"Top-Down Memoized Cost   : {min_cost_climbing_stairs_memo(rooftop_costs_1)}")
    visualize_state_transitions(rooftop_costs_1)
    
    print("=" * 50)
    
    # Test Case 2: Extended rooftop route
    rooftop_costs_2 = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
    print(f"\n[Test 2: Costs {rooftop_costs_2}]")
    print(f"Bottom-Up Optimized Cost : {min_cost_climbing_stairs_bottom_up(rooftop_costs_2)}")
    visualize_state_transitions(rooftop_costs_2)
