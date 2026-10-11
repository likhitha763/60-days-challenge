"""
Two Pointer Optimization: Remove Nth Node From End

Problem:
An encrypted communication system stores secret messages in a linked chain.
One corrupted message must be removed before transmission.

This program:
1. Builds a singly linked list message chain.
2. Removes the nth node from the end using two pointers.
3. Uses a single traversal instead of counting the list length first.
4. Explains why the single-pass approach is useful.

Time Complexity: O(L), where L is the number of messages.
Space Complexity: O(1) extra space.
"""


class Node:
    """A node representing one message in the linked chain."""

    def __init__(self, message):
        self.message = message
        self.next = None


class MessageChain:
    """Singly linked list for storing encrypted messages."""

    def __init__(self):
        self.head = None

    def build(self, messages):
        """Build the linked list from a list of messages."""
        for message in messages:
            self.append(message)

    def append(self, message):
        """Add a message to the end of the chain."""
        new_node = Node(message)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    def display(self):
        """Return the messages in the chain."""
        messages = []
        current = self.head

        while current:
            messages.append(current.message)
            current = current.next

        return messages

    def remove_nth_from_end(self, n):
        """
        Remove the nth node from the end using two pointers.

        The fast pointer is moved n steps ahead first.
        Then slow and fast move together. When fast reaches the end,
        slow is positioned just before the node that must be removed.
        """

        if n <= 0:
            raise ValueError("n must be greater than 0")

        # Dummy node makes removing the head node easy.
        dummy = Node("DUMMY")
        dummy.next = self.head

        slow = dummy
        fast = dummy

        # Create a gap of n nodes between fast and slow.
        for _ in range(n):
            fast = fast.next

            # n is larger than the list length.
            if fast is None:
                raise ValueError("n is larger than the number of messages")

        # Move both pointers together until fast reaches the last node.
        while fast.next:
            slow = slow.next
            fast = fast.next

        # slow.next is the nth node from the end.
        removed_message = slow.next.message
        slow.next = slow.next.next

        self.head = dummy.next

        return removed_message


def explain_single_pass():
    print("\nWhy does single-pass traversal matter?")
    print("- The two-pointer technique avoids traversing the list once to")
    print("  count its length and then again to find the target node.")
    print("- Fast stays n nodes ahead of slow.")
    print("- When fast reaches the end, slow is exactly where we need it.")
    print("- This reduces the operation to one traversal: O(L) time and")
    print("  O(1) extra space.")


def main():
    print("=== Encrypted Message Chain ===")

    messages = [
        "MSG-001",
        "MSG-002",
        "MSG-003",
        "MSG-004",
        "MSG-005",
    ]

    chain = MessageChain()
    chain.build(messages)

    print("Original chain:")
    print(" -> ".join(chain.display()))

    # Example: remove the 2nd message from the end.
    n = 2
    print(f"\nRemoving the {n}nd message from the end...")

    removed = chain.remove_nth_from_end(n)

    print(f"Removed message: {removed}")
    print("\nChain after removal:")
    print(" -> ".join(chain.display()))

    explain_single_pass()


if __name__ == "__main__":
    main()
