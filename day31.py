def sort_capsules(capsules: list[int]) -> list[int]:
    """
    Sorts an array containing 0s (red), 1s (white), and 2s (blue) in-place
    using the Dutch National Flag algorithm in a single pass.
    
    Parameters:
        capsules (list[int]): List of integers where 0=red, 1=white, 2=blue.
        
    Returns:
        list[int]: The sorted list (modified in-place).
    """
    # Initialize three pointers
    low = 0
    mid = 0
    high = len(capsules) - 1
    
    # Traverse the array until mid crosses high
    while mid <= high:
        if capsules[mid] == 0:
            # Red capsule: Swap to the low boundary
            capsules[low], capsules[mid] = capsules[mid], capsules[low]
            low += 1
            mid += 1
        elif capsules[mid] == 1:
            # White capsule: Already in correct middle region, just move forward
            mid += 1
        else:  # capsules[mid] == 2
            # Blue capsule: Swap to the high boundary
            capsules[mid], capsules[high] = capsules[high], capsules[mid]
            high -= 1
            # Note: mid is NOT incremented here because the swapped element 
            # from the high boundary still needs to be evaluated.
            
    return capsules

# --- Example Usage ---
if __name__ == "__main__":
    factory_belt = [2, 0, 2, 1, 1, 0, 1, 2, 0]
    print(f"Original Conveyor Belt: {factory_belt}")
    
    sort_capsules(factory_belt)
    
    print(f"Sorted Conveyor Belt:   {factory_belt}")
