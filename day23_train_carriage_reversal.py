"""
train_reversal_linked_list.py
============================================================
Phase: Linked Lists — The Runaway Train
============================================================

PROBLEM
-------
A railway company accidentally connected train carriages in the
wrong order. Each carriage is linked to the next one, like a node
in a singly linked list. The mission: reverse the entire train
without "colliding" any carriages — i.e. without losing or
corrupting any links along the way.

REAL-WORLD IMPACT
------------------
Linked lists (and the pointer-reversal technique used here) show
up constantly in real systems:
  - Memory management (free lists, garbage collectors chaining
    free memory blocks together)
  - Browser history (back/forward navigation as a doubly linked
    list of visited pages)
  - Real-time applications (undo/redo stacks, streaming buffers,
    music/video playlists)

WHAT THIS FILE DOES
--------------------
  1. Builds a linked list representation of train carriages
  2. Reverses the linked list in place
  3. Prints the original and reversed train order
  4. Explains the pointer manipulation happening at each step

APPROACH — POINTER MANIPULATION EXPLAINED
-------------------------------------------
Given a singly linked list:

    A -> B -> C -> D -> None

we want to end up with:

    D -> C -> B -> A -> None

We walk through the list once, using three pointers:

    prev    : the node that comes BEFORE current in the new
              (reversed) order. Starts as None, since the old
              head (A) will become the new tail, pointing to None.
    current : the node we are currently rewiring.
    nxt     : a temporary pointer that saves current.next BEFORE
              we overwrite it — otherwise we'd lose the rest of
              the list the moment we change current.next.

At each step:
    nxt = current.next          # save what's ahead, before we cut the link
    current.next = prev         # reverse this carriage's coupling
    prev = current               # move prev forward
    current = nxt                # move current forward (to the saved node)

This runs in O(n) time and O(1) extra space — no new nodes are
created, only existing "couplings" (next pointers) are rewired.
That's what makes it collision-free: every carriage is still
present, just facing the other way.
"""

from __future__ import annotations
from typing import Optional, List
import random


class Carriage:
    """A single train carriage — a node in the linked list."""

    def __init__(self, carriage_id):
        self.carriage_id = carriage_id
        self.next: Optional["Carriage"] = None

    def __repr__(self):
        return f"[{self.carriage_id}]"


class Train:
    """A singly linked list of train carriages, coupled front to back."""

    def __init__(self):
        self.head: Optional[Carriage] = None

    # ---------- building the train ----------

    def build_from_list(self, carriage_ids: List) -> None:
        """
        Builds the train by coupling carriages in the given order.
        carriage_ids[0] becomes the head (front) of the train.
        """
        self.head = None
        prev_carriage: Optional[Carriage] = None

        for cid in carriage_ids:
            new_carriage = Carriage(cid)
            if self.head is None:
                self.head = new_carriage
            else:
                prev_carriage.next = new_carriage
            prev_carriage = new_carriage

    def append(self, carriage_id) -> None:
        """Couples a new carriage onto the back of the train."""
        new_carriage = Carriage(carriage_id)
        if self.head is None:
            self.head = new_carriage
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_carriage

    # ---------- reversing the train ----------

    def reverse(self) -> None:
        """
        Reverses the train's coupling order in place.
        See the module docstring above for the full pointer-by-pointer
        explanation of why this works.
        """
        prev: Optional[Carriage] = None
        current: Optional[Carriage] = self.head

        while current is not None:
            nxt = current.next      # 1. save the rest of the train before cutting the link
            current.next = prev     # 2. flip this carriage's coupling to point backward
            prev = current           # 3. this carriage is now the "front" of the reversed portion
            current = nxt            # 4. move on to the next carriage in the ORIGINAL order

        self.head = prev            # the old tail is now the new head

    def reverse_with_trace(self) -> List[str]:
        """
        Same reversal logic as reverse(), but also records a
        human-readable trace of each pointer operation — useful
        for the "explain pointer manipulation" deliverable.
        """
        trace = []
        prev: Optional[Carriage] = None
        current: Optional[Carriage] = self.head
        step = 1

        while current is not None:
            nxt = current.next
            trace.append(
                f"Step {step}: at carriage {current.carriage_id} -> "
                f"save next={nxt.carriage_id if nxt else None}, "
                f"rewire {current.carriage_id}.next = "
                f"{prev.carriage_id if prev else None}, "
                f"advance prev -> {current.carriage_id}, current -> "
                f"{nxt.carriage_id if nxt else None}"
            )
            current.next = prev
            prev = current
            current = nxt
            step += 1

        self.head = prev
        return trace

    # ---------- utilities ----------

    def to_list(self) -> List:
        """Returns the train order as a plain Python list, front to back."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.carriage_id)
            current = current.next
        return result

    def __repr__(self) -> str:
        current = self.head
        parts = []
        while current is not None:
            parts.append(str(current.carriage_id))
            current = current.next
        return " -> ".join(parts) + " -> None" if parts else "None (empty train)"


# ============================================================
# Demonstrations & tests
# ============================================================

def print_train_order(label: str, train: Train) -> None:
    print(f"{label}: {train}")


def run_fixed_demo() -> None:
    print("=== Fixed demo ===")
    train = Train()
    carriage_ids = ["Engine", "C1", "C2", "C3", "C4", "Caboose"]
    train.build_from_list(carriage_ids)

    print_train_order("Original train order", train)

    print("\nPointer manipulation trace:")
    trace = train.reverse_with_trace()
    for line in trace:
        print("  " + line)

    print()
    print_train_order("Reversed train order", train)
    print()


def run_edge_case_tests() -> None:
    print("=== Edge case tests ===")

    # Empty train
    t = Train()
    t.reverse()
    assert t.to_list() == []
    print("Empty train reverses to empty train -> OK")

    # Single carriage
    t = Train()
    t.build_from_list(["OnlyCarriage"])
    t.reverse()
    assert t.to_list() == ["OnlyCarriage"]
    print("Single-carriage train unchanged after reverse -> OK")

    # Two carriages
    t = Train()
    t.build_from_list(["A", "B"])
    t.reverse()
    assert t.to_list() == ["B", "A"]
    print("Two-carriage train reverses correctly -> OK")

    # Reversing twice returns to original order
    t = Train()
    original = ["A", "B", "C", "D", "E"]
    t.build_from_list(original)
    t.reverse()
    t.reverse()
    assert t.to_list() == original
    print("Double reversal restores original order -> OK")

    print("All edge cases PASSED.\n")


def run_random_stress_test(num_trials: int = 500, max_length: int = 50, seed: int = 42) -> None:
    """
    Builds random trains of random length and checks that reversing
    the linked list always matches Python's own list reversal —
    i.e. no carriage is lost, duplicated, or mis-ordered ("collision-free").
    """
    print(f"=== Random stress test ({num_trials} trials, seed={seed}) ===")
    random.seed(seed)

    for trial in range(num_trials):
        length = random.randint(0, max_length)
        carriage_ids = [f"C{random.randint(0, 100000)}_{i}" for i in range(length)]

        train = Train()
        train.build_from_list(carriage_ids)

        expected_reversed = list(reversed(carriage_ids))
        train.reverse()
        actual_reversed = train.to_list()

        assert actual_reversed == expected_reversed, (
            f"Trial {trial} FAILED.\n"
            f"  Original: {carriage_ids}\n"
            f"  Expected: {expected_reversed}\n"
            f"  Got:      {actual_reversed}"
        )

    print(f"All {num_trials} random trials PASSED — no collisions, no lost carriages.\n")


if __name__ == "__main__":
    run_fixed_demo()
    run_edge_case_tests()
    run_random_stress_test(num_trials=500, max_length=50, seed=42)
    print("All tests completed successfully. The train has been safely reversed.")
