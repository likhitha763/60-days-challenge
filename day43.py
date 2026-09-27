"""
Project: Zombie Outbreak Escape Planner (Graph Traversal & BFS)
Problem: Shortest Path in Binary Matrix (8-directional movement)
Real-World Impact: Routing algorithms, emergency response, and navigation systems.
"""

from collections import deque

def shortest_path_binary_matrix(grid):
    """
    Finds the shortest clear path from top-left (0, 0) to bottom-right (n-1, n-1)
    in an n x n binary matrix using BFS.
    0 represents a clear road (safe), 1 represents a zombie horde/obstacle.
    """
    n = len(grid)
    
    # Check if start or end is blocked by zombies
    if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1, []

    # Queue stores tuples of (row, col, current_distance)
    queue = deque([(0, 0, 1)])
    visited = set([(0, 0)])
    
    # Parent map to reconstruct the exact path later
    parent = {(0, 0): None}

    # 8-directional movement: horizontal, vertical, and diagonal
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    while queue:
        r, c, dist = queue.popleft()

        # If we reached the rescue zone (bottom-right corner)
        if r == n - 1 and c == n - 1:
            path = []
            curr = (r, c)
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            return dist, path[::-1] # Return distance and reversed path from start to end

        # Explore all 8 adjacent neighborhood blocks
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Validate boundaries, check if it's a clear road (0), and ensure it's unvisited
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc, dist + 1))

    # If queue is exhausted and destination wasn't reached
    return -1, []

def visualize_escape_route(grid, path):
    """
    Visualizes the city grid map showing the survivor's path versus zombie blockers.
    """
    n = len(grid)
    # Create a display copy
    display = [[' 🟩 ' if cell == 0 else ' 🧟 ' for cell in row] for row in grid]
    
    # Mark the path steps
    for r, c in path:
        if (r, c) == (0, 0):
            display[r][c] = ' 🏃 '  # Survivor Start
        elif (r, c) == (n - 1, n - 1):
            display[r][c] = ' 🚁 '  # Rescue Chopper Zone
        else:
            display[r][c] = ' 👣 '  # Escape Footprints

    print("\n" + "="*40)
    print(" ZOMBIE OUTBREAK ESCAPE GRID VISUALIZATION ")
    print("="*40)
    print("Legend: 🏃 = Start | 🚁 = Rescue | 👣 = Safe Path | 🟩 = Road | 🧟 = Zombie Block\n")
    
    for row in display:
        print("".join(row))
    print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    # Example 5x5 city grid (0 = safe road, 1 = blocked by zombies)
    city_grid = [
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0]
    ]

    print("Initializing City Grid Map Scan...")
    distance, escape_path = shortest_path_binary_matrix(city_grid)

    if distance != -1:
        print(f"[SUCCESS] Shortest escape route calculated successfully!")
        print(f"Total Steps to Survival: {distance}")
        print(f"Coordinate Path: {escape_path}")
        visualize_escape_route(city_grid, escape_path)
    else:
        print("[CRITICAL WARNING] No escape route found! Survivors are entirely trapped.")
