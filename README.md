# Recursive Thinking: Staircase Paths

This project solves the classic staircase problem:

- A robot can climb either 1 or 2 steps at a time.
- The goal is to calculate how many different ways it can reach step N.

## Recursive solution

The naive recursive formula is:

```python
if n == 0:
    return 1
if n < 0:
    return 0
return count_ways_recursive(n - 1) + count_ways_recursive(n - 2)
```

This works because the robot can reach step `n` by either:

- taking one step from `n - 1`, or
- taking two steps from `n - 2`

## Why the recursive tree explodes

The recursive version recomputes the same subproblems repeatedly.
For example, when solving `ways(4)`, the recursion tree overlaps:

```text
      ways(4)
     /       \
 ways(3)   ways(2)
 /   \      /   \
2    1    1    0
```

The same smaller values like `ways(2)` and `ways(1)` are recalculated many times, so the time complexity becomes exponential.

## Memoization optimization

Memoization stores computed results so each value is solved once and reused.

```python
@lru_cache(maxsize=None)
def count_ways_memoized(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return count_ways_memoized(n - 1) + count_ways_memoized(n - 2)
```

This reduces the complexity to linear time: `O(n)`, with `O(n)` memory for the cache.

## Execution time comparison

The script compares both versions and prints the timing difference.

Example output:

```text
Target step count: 35
Recursive result: 14930352
Memoized result: 14930352
Recursive time: 0.454320 seconds
Memoized time: 0.000011 seconds
Speedup: 41392.73x
```

## Files

- `day16.py` — recursive and memoized implementations
- `test_staircase.py` — validation checks

## GitHub repository

This project can be committed to a GitHub repository using:

```bash
git init
git add .
git commit -m "Add staircase recursion and memoization solution"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Real-world impact

Recursive thinking is important in:

- AI search strategies
- pathfinding and graph traversal
- compiler design
- game engines and planning systems
