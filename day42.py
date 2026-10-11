"""
Satellite Island Counter (Number of Islands)
============================================
Phase: Graphs

Description:
A satellite system discovered hundreds of disconnected islands after a massive flood. 
This script calculates how many separate islands still exist using graph traversal 
techniques (DFS/BFS) to guide upcoming rescue missions.

Real-World Impact:
- Mapping Systems: Cartography and geographical clustering.
- Social Networks: Finding connected components and communities.
- Distributed Infrastructure: Analyzing network partitions and node connectivity.
"""

from collections import deque
import copy

def num_islands_dfs(grid: list[list[str]]) -> int:
    """
    Approach 1: Depth-First Search (DFS) Flood Fill
    ------------------------------------------------
    Iterates through the grid. When land ('1') is found, it triggers a DFS 
    to sink/mark all connected land cells as visited ('0'), incrementing the island count.
    
    Time Complexity: O(M * N) where M is rows and N is columns.
    Space Complexity: O(M * N) in the worst case due to the recursion call stack.
    """
    if not grid or not grid[0]:
        return 0
        
    rows, cols = len(grid), len(grid[0])
    island_count = 0
    
    def dfs(r, c):
        # Check boundaries and if the current cell is water ('0')
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0':
            return
        
        # Mark the current land cell as visited by turning it into water
        grid[r][c] = '0'
        
        # Traverse all 4 adjacent directions (Up, Down, Left, Right)
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                island_count += 1
                dfs(r, c)
                
    return island_count


def num_islands_bfs(grid: list[list[str]]) -> int:
    """
    Approach 2: Breadth-First Search (BFS) Queue Traversal
    -------------------------------------------------------
    Uses a queue to iteratively explore land cells level by level, sinking 
    the entire island before moving on to find the next one.
    
    Time Complexity: O(M * N)
    Space Complexity: O(min(M, N)) for the queue storage.
    """
    if not grid or not grid[0]:
        return 0
        
    rows, cols = len(grid), len(grid[0])
    island_count = 0
    
    def bfs(start_r, start_c):
        queue = deque([(start_r, start_c)])
        grid[start_r][start_c] = '0' # Mark as visited
        
        while queue:
            r, c = queue.popleft()
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                island_count += 1
                bfs(r, c)
                
    return island_count


def visualize_island_traversal(grid: list[list[str]]) -> int:
    """
    Visualizer: Demonstrates how graph traversal sweeps across the grid,
    clearing out connected land masses step-by-step.
    """
    print("\n--- Visualizing Satellite Grid Sweep ---")
    
    # Make a deep copy to preserve original grid for visualization
    sim_grid = copy.deepcopy(grid)
    rows, cols = len(sim_grid), len(sim_grid[0])
    island_count = 0
    
    def print_grid():
        for row in sim_grid:
            print(" ".join(row).replace('1', '█').replace('0', '░'))
        print("-" * 20)

    print("Initial Grid (█ = Land, ░ = Water):")
    print_grid()

    def dfs_visual(r, c, island_id):
        if r < 0 or c < 0 or r >= rows or c >= cols or sim_grid[r][c] != '1':
            return
        sim_grid[r][c] = str(island_id) # Mark with island ID for display
        
        dfs_visual(r + 1, c, island_id)
        dfs_visual(r - 1, c, island_id)
        dfs_visual(r, c + 1, island_id)
        dfs_visual(r, c - 1, island_id)

    for r in range(rows):
        for c in range(cols):
            if sim_grid[r][c] == '1':
                island_count += 1
                print(f"-> Discovered Island #{island_count} starting at position ({r}, {c})")
                dfs_visual(r, c, island_count)
                print_grid()

    return island_count


# --- Execution and Testing ---
if __name__ == "__main__":
    print("=== SATELLITE SYSTEM: POST-FLOOD ISLAND SCANNER ===")
    
    # Test Case 1: Standard Post-Flood Archipelagos
    satellite_map = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "1"],
        ["0", "0", "0", "1", "1"],
        ["0", "0", "0", "0", "0"],
        ["1", "0", "1", "1", "0"]
    ]
    
    # Create copies because DFS/BFS modify the grid in-place
    map_for_dfs = copy.deepcopy(satellite_map)
    map_for_bfs = copy.deepcopy(satellite_map)
    
    print(f"\n[Test 1: Analyzing Archipelagos]")
    print(f"Total Islands Found (DFS): {num_islands_dfs(map_for_dfs)}")
    print(f"Total Islands Found (BFS): {num_islands_bfs(map_for_bfs)}")
    
    # Run interactive visualization
    visualize_island_traversal(satellite_map)


"""
--- LINKEDIN REFLECTION ---
Post Title: Turning Graph Theory into Real-World Rescue Missions 🗺️🛰️

Graph traversal isn't just an abstract interview concept—it's how we solve real-world 
logistics crises. Today, I tackled the 'Number of Islands' problem, simulating a post-flood 
satellite mapping scenario where automated systems must identify disconnected landmasses 
to dispatch emergency rescue teams.

Using Depth-First Search (DFS) and Breadth-First Search (BFS) flood-fill algorithms, 
we can traverse 2D grid matrices in O(M * N) time while keeping auxiliary memory efficient. 
Whether you're mapping islands after a natural disaster, optimizing social network clusters, 
or tracking database partitions, graph algorithms form the backbone of connected systems! 

#SoftwareEngineering #GraphTheory #Algorithms #ProblemSolving #Python #CodingJourney
"""
