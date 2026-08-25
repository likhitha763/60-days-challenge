def reverse_string(text):
    """
    Return the reverse of a string.

    Time Complexity: O(n)
    Space Complexity: O(n), because a new reversed string is created.
    """
    return text[::-1]


def analyze_space_usage(text):
    """
    Analyze whitespace usage in a string.

    Time Complexity: O(n)
    Space Complexity: O(1), excluding the returned summary dictionary.
    """
    spaces = 0
    tabs = 0
    newlines = 0

    for character in text:
        if character == " ":
            spaces += 1
        elif character == "\t":
            tabs += 1
        elif character == "\n":
            newlines += 1

    total_whitespace = spaces + tabs + newlines

    return {
        "characters": len(text),
        "spaces": spaces,
        "tabs": tabs,
        "newlines": newlines,
        "total_whitespace": total_whitespace,
    }


# Example usage:
if __name__ == "__main__":
    message = "Hello world from Day 12"

    print("Original string:", message)
    print("Reversed string:", reverse_string(message))

    usage = analyze_space_usage(message)
    print("Space usage analysis:")
    print("Characters:", usage["characters"])
    print("Spaces:", usage["spaces"])
    print("Tabs:", usage["tabs"])
    print("Newlines:", usage["newlines"])
    print("Total whitespace:", usage["total_whitespace"])
