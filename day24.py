"""
Merging Systems Challenge
==========================

Two kingdoms maintain sorted records of their soldiers (as sorted linked
lists). This program merges both armies into a single, perfectly sorted
master list without losing order.

Merge Strategy
---------------
This is the classic two-pointer merge used in merge sort / database merge
joins:

1. Keep a pointer into each list (list A, list B).
2. At each step, compare the current node's value in A with the current
   node's value in B.
3. Append the smaller value to the result list and advance that list's
   pointer.
4. If both values are equal, append the value once (or twice, depending on
   the `keep_duplicates` flag below) and advance BOTH pointers.
5. When one list runs out, append all remaining nodes from the other list
   directly, since it is already sorted.

This runs in O(n + m) time and O(1) extra space (aside from the new nodes
created for the result), where n and m are the lengths of the two lists.

Duplicate Handling
-------------------
By default, duplicate values across the two lists are kept (so the result
length = len(A) + len(B)). Set `keep_duplicates=False` in `merge_sorted`
to collapse equal values into a single occurrence in the merged list.

Real-World Impact
-------------------
This exact pattern is used in:
- Databases: merge joins on sorted indexes.
- Distributed systems: merging sorted shards/partitions of data.
- Search engines: merging sorted posting lists during query evaluation.
"""

from __future__ import annotations
from typing import Optional, Iterable, List


class Node:
    """A single node in a singly linked list."""

    def __init__(self, value: int):
        self.value = value
        self.next: Optional["Node"] = None

    def __repr__(self) -> str:
        return f"Node({self.value})"


class LinkedList:
    """A simple singly linked list that stays sorted as you build it."""

    def __init__(self, values: Optional[Iterable[int]] = None):
        self.head: Optional[Node] = None
        if values:
            for v in sorted(values):
                self.append(v)

    def append(self, value: int) -> None:
        """Append a value to the end of the list (assumes caller keeps it sorted)."""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def to_list(self) -> List[int]:
        """Return the linked list's values as a plain Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def __repr__(self) -> str:
        return " -> ".join(str(v) for v in self.to_list()) or "(empty)"


def merge_sorted(list_a: LinkedList, list_b: LinkedList,
                  keep_duplicates: bool = True) -> LinkedList:
    """
    Merge two sorted LinkedLists into one sorted LinkedList.

    Args:
        list_a: First sorted linked list (e.g., Kingdom A's soldiers).
        list_b: Second sorted linked list (e.g., Kingdom B's soldiers).
        keep_duplicates: If True (default), duplicate values from both
            lists are all kept in the result. If False, equal values are
            collapsed into a single entry.

    Returns:
        A new LinkedList containing all values from both lists in sorted
        order.
    """
    merged = LinkedList()
    a = list_a.head
    b = list_b.head

    while a is not None and b is not None:
        if a.value < b.value:
            merged.append(a.value)
            a = a.next
        elif a.value > b.value:
            merged.append(b.value)
            b = b.next
        else:  # a.value == b.value -> duplicate across the two lists
            merged.append(a.value)
            if keep_duplicates:
                merged.append(b.value)
            a = a.next
            b = b.next

    # One list is exhausted; the remainder of the other is already sorted.
    remaining = a if a is not None else b
    while remaining is not None:
        merged.append(remaining.value)
        remaining = remaining.next

    return merged


def _demo() -> None:
    """Small demo showing the merge in action, including duplicates."""
    kingdom_a = LinkedList([1, 3, 5, 7, 9])
    kingdom_b = LinkedList([2, 3, 6, 7, 10])

    print("Kingdom A soldiers:", kingdom_a)
    print("Kingdom B soldiers:", kingdom_b)

    merged_with_dupes = merge_sorted(kingdom_a, kingdom_b, keep_duplicates=True)
    print("\nMerged (keeping duplicates):")
    print(merged_with_dupes)

    merged_no_dupes = merge_sorted(kingdom_a, kingdom_b, keep_duplicates=False)
    print("\nMerged (duplicates collapsed):")
    print(merged_no_dupes)


if __name__ == "__main__":
    _demo()
