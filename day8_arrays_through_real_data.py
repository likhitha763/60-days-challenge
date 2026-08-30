"""Day 8: Arrays Through Real Data

Goal:
Create a list of numbers that simulates user data and count how many numbers
contain only even digits.

This mirrors how systems track user activity, analytics metrics, and other
numeric datasets in the real world.
"""


def has_even_digits(number: int) -> bool:
    """Return True if every digit in the number is even."""
    if number < 0:
        number = abs(number)

    if number == 0:
        return True

    digits = [int(digit) for digit in str(number)]
    return all(digit % 2 == 0 for digit in digits)


def count_even_digit_numbers(data: list[int]) -> list[int]:
    """Return only the numbers where every digit is even."""
    return [value for value in data if has_even_digits(value)]


def main() -> None:
    user_activity = [124, 48, 3, 22, 302, 77, 84, 19, 50, 246]

    even_digit_numbers = count_even_digit_numbers(user_activity)

    print("Simulated user data:")
    print(user_activity)
    print()
    print("Numbers with only even digits:")
    print(even_digit_numbers)
    print()
    print(f"Total matching numbers: {len(even_digit_numbers)}")
    print()
    print("Why arrays matter in real systems:")
    print(
        "Arrays store large collections of related values such as user IDs, "
        "click counts, sensor readings, or log entries. They make it easy to "
        "loop through and analyze data quickly in dashboards, analytics tools, "
        "and tracking systems."
    )


if __name__ == "__main__":
    main()
