"""
Name: day19_vault_temperature.py
Description: A Min Stack implementation to track and instantly retrieve the 
             minimum temperature in O(1) time complexity.
"""

class MinStack:
    """
    A stack that supports push, pop, top, and retrieving the minimum element in O(1) time.
    """
    def __init__(self):
        # Main stack to store all temperature readings
        self.stack = []
        # Auxiliary stack to keep track of the minimum values
        self.min_stack = []

    def push(self, val: int) -> None:
        """Push a temperature reading onto the vault."""
        self.stack.append(val)
        # If min_stack is empty or the new value is less than or equal 
        # to the current minimum, push it onto the min_stack.
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        """Remove the top temperature reading from the vault."""
        if not self.stack:
            raise IndexError("Vault is empty. Cannot pop from an empty stack.")
        
        popped_val = self.stack.pop()
        # If the popped value is the current minimum, remove it from min_stack as well
        if popped_val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        """Get the most recent temperature reading."""
        if not self.stack:
            raise IndexError("Vault is empty.")
        return self.stack[-1]

    def get_min(self) -> int:
        """Retrieve the minimum temperature recorded in O(1) time."""
        if not self.min_stack:
            raise IndexError("Vault is empty.")
        return self.min_stack[-1]


# ==========================================
# README Explanation & Testing
# ==========================================
if __name__ == "__main__":
    """
    README & Testing Suite for the Futuristic Vault Temperature System
    
    ## Overview
    This module implements a specialized `MinStack` data structure designed to record 
    temperature readings every second and instantly return the minimum recorded temperature 
    at any given moment with $O(1)$ time complexity.

    ## How It Works (The Two-Stack Approach)
    1. **Main Stack (`self.stack`)**: Functions like a standard stack, recording every 
       incoming temperature sequentially.
    2. **Min Stack (`self.min_stack`)**: Tracks historical minimums. Whenever a new 
       temperature is pushed, it is only added to `min_stack` if it is less than or 
       equal to the current minimum. When popping, if the removed value matches the top 
       of `min_stack`, it is removed from there as well.
    
    ## Complexity
    - **Time Complexity**: $O(1)$ for `push`, `pop`, `top`, and `get_min`.
    - **Space Complexity**: $O(N)$ to store elements across both stacks.
    """

    print("--- Initializing Futuristic Vault Temperature System ---")
    vault = MinStack()

    # Test inputs: simulating temperature readings over time
    readings = [22, 15, 30, 10, 10, 25]
    print(f"\nPushing temperature readings sequentially: {readings}")

    for temp in readings:
        vault.push(temp)
        print(f"Pushed: {temp} | Current Minimum: {vault.get_min()}")

    print("\n--- Testing Pop Operations ---")
    while vault.stack:
        current_min = vault.get_min()
        top_val = vault.top()
        print(f"Top: {top_val} | Current Min before pop: {current_min}")
        vault.pop()
        if vault.stack:
            print(f"-> Popped {top_val}. New Minimum: {vault.get_min()}\n")
        else:
            print(f"-> Popped {top_val}. Vault is now empty.")
