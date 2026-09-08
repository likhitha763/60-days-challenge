"""
Cycle Detection in Maze Paths
Phase: Cycle Detection

Concept:
A maze path is represented using a linked list. Each node represents
a position in the maze and points to the next position.

We use Floyd's Cycle Detection Algorithm:
    - Slow pointer moves 1 step at a time.
    - Fast pointer moves 2 steps at a time.
    - If they meet, a cycle exists.
    - If fast reaches None, there is no cycle.

Real-world impact:
Cycle detection is useful for preventing infinite loops in:
    - Operating systems
    - Dependency graphs
    - Distributed systems
    - Linked lists
    - Game/map navigation
"""


# ---------------------------------------------------------
# 1. Linked List Node
# ---------------------------------------------------------

class MazeNode:
    """Represents one position/path in the maze."""

    def __init__(self, position):
        self.position = position
        self.next = None


# ---------------------------------------------------------
# 2. Create a Maze Path
# ---------------------------------------------------------

def create_maze_path(positions, cycle_to=None):
    """
    Create a linked-list maze path.

    positions:
        List of maze positions, e.g. ["Start", "A", "B", "Exit"]

    cycle_to:
        Index of the node where the last node should point.
        None means the path ends normally.

    Example:
        ["Start", "A", "B", "C"], cycle_to=1

        Start -> A -> B -> C
                  ^         |
                  |_________|
    """

    if not positions:
        return None

    nodes = [MazeNode(position) for position in positions]

    # Connect nodes normally
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]

    # Create a cycle if requested
    if cycle_to is not None:
        if 0 <= cycle_to < len(nodes):
            nodes[-1].next = nodes[cycle_to]
        else:
            raise ValueError("cycle_to index is out of range.")

    return nodes[0]


# ---------------------------------------------------------
# 3. Floyd's Cycle Detection Algorithm
# ---------------------------------------------------------

def detect_cycle(head):
    """
    Detect whether the maze path contains a cycle.

    Returns:
        True  -> Cycle exists
        False -> No cycle
    """

    slow = head
    fast = head

    while fast is not None and fast.next is not None:

        # Slow moves one step
        slow = slow.next

        # Fast moves two steps
        fast = fast.next.next

        # If they meet, a cycle exists
        if slow is fast:
            return True

    return False


# ---------------------------------------------------------
# 4. Find Where the Cycle Starts
# ---------------------------------------------------------

def find_cycle_start(head):
    """
    Finds the node where the cycle begins.

    Uses Floyd's algorithm.

    Returns:
        MazeNode -> starting node of cycle
        None     -> no cycle
    """

    slow = head
    fast = head

    # First phase: detect meeting point
    while fast is not None and fast.next is not None:

        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            break
    else:
        return None

    # Second phase:
    # Move one pointer back to the head.
    # Move both one step at a time.
    slow = head

    while slow is not fast:
        slow = slow.next
        fast = fast.next

    return slow


# ---------------------------------------------------------
# 5. Simulate Maze Movement
# ---------------------------------------------------------

def simulate_maze(head, max_steps=15):
    """
    Simulates a player moving through the maze.

    max_steps prevents the program itself from running
    forever if a cycle exists.
    """

    current = head
    visited_positions = []

    print("\nMaze Simulation")
    print("-" * 40)

    for step in range(max_steps):

        if current is None:
            print("Player reached the end of the maze.")
            return

        print(f"Step {step + 1}: {current.position}")
        visited_positions.append(current.position)

        current = current.next

    print("\nSimulation stopped after maximum steps.")
    print("This protects the program from an infinite loop.")

    if detect_cycle(head):
        print("⚠️ Infinite cycle detected!")
    else:
        print("No cycle detected.")


# ---------------------------------------------------------
# 6. Test Multiple Maze Configurations
# ---------------------------------------------------------

def test_maze_configurations():

    configurations = [
        {
            "name": "Maze 1 - Safe Path",
            "positions": ["Start", "Hall A", "Hall B", "Exit"],
            "cycle_to": None
        },
        {
            "name": "Maze 2 - Simple Loop",
            "positions": ["Start", "Room A", "Room B", "Room C"],
            "cycle_to": 1
        },
        {
            "name": "Maze 3 - Loop Back to Start",
            "positions": ["Start", "Room A", "Room B"],
            "cycle_to": 0
        },
        {
            "name": "Maze 4 - Longer Safe Path",
            "positions": [
                "Start",
                "Hall A",
                "Hall B",
                "Hall C",
                "Hall D",
                "Exit"
            ],
            "cycle_to": None
        },
        {
            "name": "Maze 5 - Loop Near the End",
            "positions": [
                "Start",
                "Room A",
                "Room B",
                "Room C",
                "Room D"
            ],
            "cycle_to": 2
        }
    ]

    print("=" * 60)
    print("        MAZE CYCLE DETECTION SYSTEM")
    print("=" * 60)

    for maze in configurations:

        print(f"\n{maze['name']}")
        print("-" * 60)

        head = create_maze_path(
            maze["positions"],
            maze["cycle_to"]
        )

        # Detect cycle
        has_cycle = detect_cycle(head)

        if has_cycle:
            print("Result: ⚠️ CYCLE DETECTED")

            cycle_start = find_cycle_start(head)

            if cycle_start:
                print(f"Cycle starts at: {cycle_start.position}")

            print("Status: Player may be trapped!")
        else:
            print("Result: ✅ NO CYCLE")
            print("Status: Player can eventually reach the end.")

        # Show simulation
        simulate_maze(head)


# ---------------------------------------------------------
# 7. Explain Why Cycle Detection Matters
# ---------------------------------------------------------

def explain_importance():

    print("\n")
    print("=" * 60)
    print("WHY CYCLE DETECTION MATTERS")
    print("=" * 60)

    print("""
1. VIDEO GAMES
   A player could enter a path that sends them around the
   same rooms forever. Detecting the cycle helps the game
   prevent broken or impossible levels.

2. OPERATING SYSTEMS
   Cycles can appear in resource dependencies.
   For example:
       Process A -> waits for B
       Process B -> waits for A

   Detecting the cycle can help identify deadlocks.

3. DEPENDENCY GRAPHS
   Software packages may depend on one another.

       Package A -> Package B -> Package C -> Package A

   This creates a circular dependency.

4. DISTRIBUTED SYSTEMS
   Distributed services can create circular dependencies
   or message flows. Detecting cycles can prevent systems
   from repeatedly processing the same path.

5. LINKED LISTS
   A linked list that accidentally points back to an earlier
   node can cause traversal to continue forever.

Floyd's algorithm is useful because it:
   - Uses O(1) extra memory
   - Runs in O(n) time
   - Does not require a separate