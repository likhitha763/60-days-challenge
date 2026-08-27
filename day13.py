def is_anagram_hashmap(s1, s2):
    """
    Solves the anagram problem using a Hashmap (Dictionary) in O(N) time.
    """
    if len(s1) != len(s2):
        return False

    char_count = {}

    # Count frequencies for characters in the first string
    for char in s1:
        char_count[char] = char_count.get(char, 0) + 1

    # Subtract frequencies using the second string
    for char in s2:
        if char not in char_count or char_count[char] == 0:
            return False
        char_count[char] -= 1

    return True


def is_anagram_brute_force(s1, s2):
    """
    Solves the anagram problem using sorting (Brute Force / Comparison approach) 
    in O(N log N) time.
    """
    return sorted(s1) == sorted(s2)


# Example usage & comparison
if __name__ == "__main__":
    string1 = "listen"
    string2 = "silent"

    print(f"Hashmap approach result: {is_anagram_hashmap(string1, string2)}")
    print(f"Brute force approach result: {is_anagram_brute_force(string1, string2)}")