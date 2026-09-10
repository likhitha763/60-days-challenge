"""
Bot / Duplicate Activity Detection Within K Distance
=====================================================
Problem: given a sequence of social media post events, flag any post whose
content repeats another post within K positions of it in the stream (i.e.
the same content posted twice, close together -- classic spam/bot signal).

"Within K distance" here means K *positions* apart in the event stream,
not K seconds -- see the note at the top of the conversation for why that
interpretation was chosen over a timestamp-based one.

Two implementations:
1. brute_force_check  -- O(n*k) time: for each event, scan back up to k prior events.
2. hash_based_check   -- O(n) time:   for each event, one hash-map lookup.

Both find the SAME first violation, so correctness is directly comparable.
"""

import random
import time


# ---------------------------------------------------------------------------
# Event simulation
# ---------------------------------------------------------------------------

def simulate_events(n: int, num_distinct_contents: int, seed: int = 42) -> list:
    """
    Generate `n` simulated post events as content labels (e.g. a hash of the
    post body -- represented here as a string id standing in for that hash).
    Fewer distinct contents relative to n means more repeats are likely,
    simulating a bot reposting a small set of messages repeatedly.
    """
    rng = random.Random(seed)
    return [f"content-{rng.randint(0, num_distinct_contents - 1)}" for _ in range(n)]


def guaranteed_unique_events(n: int) -> list:
    """
    Deterministically unique content labels -- no randomness, no reliance on
    a 'low enough' collision probability. This is the true worst case: with
    zero duplicates possible, neither algorithm can ever exit early, so the
    full O(n) / O(n*k) cost is always paid. Used only for benchmarking, where
    accidental early exits (via birthday-paradox collisions) would corrupt
    the timing comparison.
    """
    return [f"unique-{i}" for i in range(n)]


# ---------------------------------------------------------------------------
# Brute force: O(n * k)
# ---------------------------------------------------------------------------

def brute_force_check(events: list, k: int):
    """
    For each event, manually scan the previous k events looking for a match.
    Returns (True, i, j) for the first violation found (i is the later index,
    j the earlier one), or (False, None, None) if no violation exists.
    """
    n = len(events)
    for i in range(n):
        window_start = max(0, i - k)
        for j in range(window_start, i):
            if events[i] == events[j]:
                return True, i, j
    return False, None, None


# ---------------------------------------------------------------------------
# Optimized: O(n) using a hash map of "content -> last seen index"
# ---------------------------------------------------------------------------

def hash_based_check(events: list, k: int):
    """
    Single pass. For each event, check the hash map for when this exact
    content was last seen. If that was within k positions, it's a violation.
    Otherwise, record/update the last-seen index and move on.

    This never re-scans anything -- each event is looked at exactly once,
    and the hash map lookup is O(1) on average.
    """
    last_seen = {}
    for i, content in enumerate(events):
        if content in last_seen and i - last_seen[content] <= k:
            return True, i, last_seen[content]
        last_seen[content] = i
    return False, None, None


# ---------------------------------------------------------------------------
# Correctness tests
# ---------------------------------------------------------------------------

def run_tests():
    # No duplicates at all
    events = ["a", "b", "c", "d"]
    assert brute_force_check(events, 2) == (False, None, None)
    assert hash_based_check(events, 2) == (False, None, None)

    # Duplicate exactly at distance k (should count -- "within k" is inclusive)
    events = ["a", "b", "c", "a"]  # distance from index 3 to 0 is 3
    assert brute_force_check(events, 3) == (True, 3, 0)
    assert hash_based_check(events, 3) == (True, 3, 0)

    # Same duplicate, but k too small to catch it
    assert brute_force_check(events, 2) == (False, None, None)
    assert hash_based_check(events, 2) == (False, None, None)

    # Duplicate right next to each other (distance 1)
    events = ["a", "a", "b", "c"]
    assert brute_force_check(events, 1) == (True, 1, 0)
    assert hash_based_check(events, 1) == (True, 1, 0)

    # Repeated content but far apart -- should NOT trigger with small k
    events = ["a", "b", "c", "d", "e", "a"]
    assert brute_force_check(events, 2) == (False, None, None)
    assert hash_based_check(events, 2) == (False, None, None)
    # ... but should trigger if k is large enough to span the gap
    assert brute_force_check(events, 5) == (True, 5, 0)
    assert hash_based_check(events, 5) == (True, 5, 0)

    # Empty stream
    assert brute_force_check([], 3) == (False, None, None)
    assert hash_based_check([], 3) == (False, None, None)

    print("PASS: all 7 correctness cases (brute force and hash-based agree)")

    # Cross-check both implementations agree on random data
    for trial in range(15):
        rng = random.Random(trial)
        events = simulate_events(n=rng.randint(0, 100), num_distinct_contents=rng.randint(1, 20), seed=trial)
        k = rng.randint(1, 10)
        bf = brute_force_check(events, k)
        hb = hash_based_check(events, k)
        assert bf == hb, f"mismatch at trial {trial}: brute={bf} hash={hb}"

    print("PASS: 15 random cross-validation trials (brute force and hash agree)")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark():
    print("\nBenchmark: brute force O(n*k) vs hash-based O(n)")
    print(f"{'n':>10} | {'k':>4} | {'brute force (s)':>16} | {'hash-based (s)':>14}")
    print("-" * 54)

    # Fixed, moderate k -- brute force cost still grows with n even though
    # k is constant, because it's O(n*k), not O(k) alone.
    k = 50
    for n in [1_000, 5_000, 10_000, 20_000, 50_000]:
        # Deterministic uniqueness, not "probably unique" -- see docstring.
        events = guaranteed_unique_events(n)

        start = time.perf_counter()
        brute_force_check(events, k)
        bf_time = time.perf_counter() - start

        start = time.perf_counter()
        hash_based_check(events, k)
        hb_time = time.perf_counter() - start

        print(f"{n:>10} | {k:>4} | {bf_time:>16.4f} | {hb_time:>14.6f}")

    # Now hold n fixed and grow k, to isolate k's effect on brute force.
    print("\nHolding n fixed, growing k (isolates k's cost in brute force):")
    print(f"{'n':>10} | {'k':>6} | {'brute force (s)':>16} | {'hash-based (s)':>14}")
    print("-" * 56)
    n = 20_000
    for k in [10, 100, 500, 2_000]:
        # Deterministic uniqueness -- see guaranteed_unique_events docstring.
        # A "large enough" random pool is NOT sufficient here: with 20,000
        # draws, the birthday paradox still gives a meaningful chance of an
        # accidental match even from a pool of millions, which is exactly
        # what corrupted the previous version of this benchmark.
        events = guaranteed_unique_events(n)
        start = time.perf_counter()
        brute_force_check(events, k)
        bf_time = time.perf_counter() - start

        start = time.perf_counter()
        hash_based_check(events, k)
        hb_time = time.perf_counter() - start

        print(f"{n:>10} | {k:>6} | {bf_time:>16.4f} | {hb_time:>14.6f}")


# ---------------------------------------------------------------------------
# Explanation
# ---------------------------------------------------------------------------

EXPLANATION = """
Why hashing improves performance here
---------------------------------------
Brute force answers "have I seen this content in the last k events?" by
re-scanning up to k prior events, every single time -- that's O(n*k)
overall. The benchmark above shows this directly: holding k fixed but
growing n, brute force's time grows linearly with n (as expected), but
growing k while holding n fixed ALSO makes it slower -- because k controls
how much re-scanning happens per event, not just a constant.

The hash-based version answers the same question with a single dictionary
lookup: "what index did I last see this exact content at?" That's O(1)
average time regardless of how big k is, because a hash map doesn't scan
anything -- it computes where to look. The whole pass is O(n) and, unlike
brute force, is completely insensitive to how large the detection window
(k) is.

This matters for real spam/bot detection because k (the "suspicious
window") is a business decision, not a fixed constant -- platforms may
want to check for duplicates within the last 100 posts, or the last
10,000. A brute-force approach gets proportionally slower as that window
grows; a hash-based approach doesn't care.
"""


if __name__ == "__main__":
    run_tests()
    benchmark()
    print(EXPLANATION)
