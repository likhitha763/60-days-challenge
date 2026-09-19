# ==========================================
# Challenge: Container With Most Water
# Phase: Two Pointer Optimization
# ==========================================

def max_area_optimized(height: list[int]) -> int:
    """
    Optimized Two-Pointer Solution.
    
    Explanation:
    - We initialize two pointers: `left` at the beginning (0) and `right` at the end (len - 1).
    - The area of water is determined by the distance between the lines (`right - left`) 
      multiplied by the height of the shorter wall (`min(height[left], height[right])`).
    - Why move the smaller wall? 
      The area is limited by the shorter wall. Moving the taller wall inward can only decrease 
      the width while keeping the limiting height the same or lower, which cannot yield a larger area. 
      Therefore, to find a potentially higher container, we must greedily move the pointer of the 
      shorter wall inward.
      
    Time Complexity: O(n) - Single pass through the array.
    Space Complexity: O(1) - Constant extra space used.
    """
    left = 0
    right = len(height) - 1
    max_water = 0

    while left < right:
        width = right - left
        current_height = min(height[left], height[right])
        current_water = width * current_height
        
        # Update maximum water found
        max_water = max(max_water, current_water)
        
        # Move the smaller wall inward
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
            
    return max_water


def max_area_brute_force(height: list[int]) -> int:
    """
    Brute-Force Solution (for comparison).
    
    Explanation:
    - Checks every possible pair of lines to calculate the area of water they can hold.
    
    Time Complexity: O(n^2) - Nested loops checking all pairs.
    Space Complexity: O(1) - Constant space.
    """
    max_water = 0
    n = len(height)
    for i in range(n):
        for j in range(i + 1, n):
            width = j - i
            current_height = min(height[i], height[j])
            max_water = max(max_water, width * current_height)
    return max_water


if __name__ == "__main__":
    # Sample test case
    sample_heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    
    print("--- Container With Most Water ---")
    print(f"Heights: {sample_heights}\n")
    
    opt_result = max_area_optimized(sample_heights)
    bf_result = max_area_brute_force(sample_heights)
    
    print(f"Optimized Two-Pointer Result: {opt_result}")
    print(f"Brute-Force Result:          {bf_result}")
