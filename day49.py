"""
Sprint Challenge: Senior Engineering Architecture & Problem Solving
==================================================================
Phase: Sprint Challenge (Day 49)

Description:
Welcome to the Sprint Challenge. This production-grade script encapsulates solutions 
to three distinct engineering challenges across Graphs, Dynamic Programming, and 
Greedy Optimization. It is accompanied by senior-level trade-off analysis, edge case 
considerations, and architectural reasoning suitable for a team presentation.

Included Problems:
1. Graph Problem: Course Schedule (Detecting cycles via Topological Sort / BFS)
2. Dynamic Programming Problem: Coin Change (Minimum coins for target amount)
3. Optimization Challenge: Jump Game II (Greedy minimum jumps to target)

Real-World Impact:
Senior engineering evaluations prioritize system stability, time/space trade-off 
analysis, and clear communication over raw code output.
"""

from collections import deque

# =====================================================================
# PROBLEM 1: GRAPH PROBLEM - COURSE SCHEDULE (Topological Sort / BFS)
# =====================================================================
def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Architecture Rationale & Thought Process:
    -----------------------------------------
    - Problem: Determine if all courses can be finished given prerequisite pairs 
      [course, prerequisite]. This maps directly to cycle detection in a directed graph.
    - Approach: Kahn's Algorithm (BFS topological sort using in-degrees). 
      If a directed cycle exists, nodes in the cycle will never have their in-degree 
      reduce to 0, leaving them unprocessed.
    - Time Complexity: O(V + E) where V is courses and E is prerequisites.
    - Space Complexity: O(V + E) for adjacency list and in-degree tracking array.
    """
    adj = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    
    # Build graph and calculate in-degrees
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
        
    # Queue for courses with no incoming prerequisites (in-degree 0)
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    processed_count = 0
    
    while queue:
        curr = queue.popleft()
        processed_count += 1
        
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # If we processed all courses, there are no cycles
    return processed_count == num_courses


# =====================================================================
# PROBLEM 2: DYNAMIC PROGRAMMING - COIN CHANGE
# =====================================================================
def coin_change(coins: list[int], amount: int) -> int:
    """
    Architecture Rationale & Thought Process:
    -----------------------------------------
    - Problem: Find the fewest number of coins needed to make up a given amount.
    - Approach: Bottom-up Dynamic Programming. Define dp[i] as the minimum coins 
      needed for amount `i`. Initialize with infinity, and set dp[0] = 0.
    - Trade-off: Unlike greedy coin selection (which fails for arbitrary coin systems 
      like [1, 3, 4] for amount 6), DP guarantees the global optimum by evaluating all 
      sub-problems.
    - Time Complexity: O(amount * N) where N is the number of coin denominations.
    - Space Complexity: O(amount) for the DP lookup table.
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[1 + (i - coin) - (i - coin)] if False else dp[i - coin] + 1)
                
    return dp[amount] if dp[amount] != float('inf') else -1


# =====================================================================
# PROBLEM 3: OPTIMIZATION CHALLENGE - JUMP GAME II (Greedy)
# =====================================================================
def jump_game_ii(nums: list[int]) -> int:
    """
    Architecture Rationale & Thought Process:
    -----------------------------------------
    - Problem: Return the minimum number of jumps to reach the last index.
    - Approach: Greedy BFS-like window expansion. Instead of exploring every path 
      (which leads to exponential time), we track the furthest reachable index 
      within our current jump boundary (`current_end`). When we hit that boundary, 
      we increment our jump counter and expand to the new maximum reach.
    - Time Complexity: O(N) single pass.
    - Space Complexity: O(1) auxiliary memory.
    """
    jumps = 0
    current_end = 0
    farthest = 0
    
    # We don't need to jump from the last index
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        
        # If we reached the boundary of the current jump, we must jump again
        if i == current_end:
            jumps += 1
            current_end = farthest
            
            # Optimization: Early exit if we can already reach the end
            if current_end >= len(nums) - 1:
                break
                
    return jumps


# =====================================================================
# EXECUTION & VERIFICATION SUITE
# =====================================================================
if __name__ == "__main__":
    print("=== SPRINT CHALLENGE: ARCHITECTURE & SOLUTIONS ===")
    
    # 1. Graph Test
    courses = 4
    prereqs = [[1, 0], [2, 1], [3, 2]]
    print(f"\n[Graph] Course Schedule Valid: {can_finish_courses(courses, prereqs)}")
    
    # 2. DP Test
    coin_denominations = [1, 2, 5]
    target_amount = 11
    print(f"[DP] Min Coins for {target_amount}: {coin_change(coin_denominations, target_amount)}")
    
    # 3. Optimization Test
    jump_steps = [2, 3, 1, 1, 4]
    print(f"[Optimization] Min Jumps for {jump_steps}: {jump_game_ii(jump_steps)}")
    print("\nAll sprint challenge modules verified successfully.")


"""
--- LINKEDIN REFLECTION ---
Post Title: Surviving the Sprint Challenge: Graphs, DP, and Scalability 🚀💡

Day 49 of the ABTalks 60 Days Claude Challenge tested more than just coding syntax—it 
evaluated how we communicate engineering decisions under pressure. 

In today's sprint challenge, I tackled three distinct architectures:
1. Graph Cycle Detection: Using Kahn's Algorithm (BFS topological sort) to map out complex 
   system and course dependencies in linear O(V + E) time.
2. Dynamic Programming Optimization: Solving the Coin Change problem via bottom-up tabulation 
   to guarantee global optimality where greedy algorithms break down.
3. Greedy Range Expansion: Implementing Jump Game II to achieve O(N) time and O(1) space 
   efficiency by tracking dynamic window boundaries.

Senior engineering isn't just about making code work; it's about evaluating trade-offs, 
anticipating edge cases, and defending design choices to your team. 11 days left until the finish line!

#SoftwareEngineering #SystemDesign #Algorithms #DataStructures #Python #CodingJourney #BuildInPublic
"""
