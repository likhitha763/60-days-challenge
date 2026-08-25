def move_zeroes(nums):
    """
    Move all zeroes to the end of the list in-place while maintaining
    the relative order of non-zero elements.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    insert_pos = 0

    for current in range(len(nums)):
        if nums[current] != 0:
            nums[insert_pos], nums[current] = nums[current], nums[insert_pos]
            insert_pos += 1

    return nums


# Example usage:
if __name__ == "__main__":
    numbers = [0, 1, 0, 3, 12]
    print("Before:", numbers)
    move_zeroes(numbers)
    print("After: ", numbers)
