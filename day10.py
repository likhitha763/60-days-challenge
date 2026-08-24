def max_subarray_sum(nums):
    """
    Solves the maximum subarray problem using Kadane's Algorithm.
    Tracks the running sum and updates the maximum sum found so far.
    """
    if not nums:
        return 0

    current_sum = max_sum = nums[0]

    for num in nums[1:]:
        # Decide whether to add the current number to the existing subarray
        # or start a new subarray from the current element.
        current_sum = max(num, current_sum + num)
        
        # Update the global maximum sum if the current running sum is greater
        max_sum = max(max_sum, current_sum)

    return max_sum

# Example usage:
if __name__ == "__main__":
    sample_array = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    result = max_subarray_sum(sample_array)
    print(f"The maximum contiguous subarray sum is: {result}")