# Day 58: Mock Interview Arena

## Interview format

Suggested 45-minute run:

- 20 minutes: solve the DSA problem and explain the invariant before coding.
- 10 minutes: reproduce and repair the debugging failure.
- 15 minutes: discuss the URL-shortener design and its tradeoffs.

Keep narrating decisions, assumptions, edge cases, and complexity as you work.
The answers below are a reference submission, not a script to memorize.

## 1. Timed DSA: Longest Substring Without Repeating Characters

Given a string, return the length of its longest contiguous substring with all
distinct characters. For example, `"abcabcbb"` returns `3` (`"abc"`).

### Reasoning

I will use a sliding window whose current contents contain no duplicates. A
dictionary records the most recent index of each character. When a character
repeats inside the window, I move the left boundary just past its previous
index; otherwise the boundary stays put. I update the best length after each
character.

The invariant is that the window from `window_start` through the current index
has unique characters. The `previous_index >= window_start` check matters: a
duplicate that lies to the left of the current window must not move its start
backward. This handles inputs such as `"abba"`.

The scan is O(n) time because each character is processed once. The dictionary
uses O(min(n, alphabet_size)) space. Empty input returns zero; a single
character returns one.

## 2. Debugging: Binary Search Boundary Bug

The intentionally broken `broken_binary_search` is in `day58.py`. Its loop
uses `left < right`, so it exits when one candidate remains without checking
that candidate. For `[2, 4, 7, 9]` and target `9`, it incorrectly returns
`-1`.

I changed the condition to `left <= right`. That keeps the final candidate in
the search interval until it has been checked. Each branch still strictly
shrinks the interval, so the search terminates. I also checked the first and
last elements, a missing target, and an empty list. Complexity is O(log n)
time and O(1) extra space.

## 3. System Design: URL Shortener

### Requirements and assumptions

- Accept a long URL and return a short URL.
- Redirect a short code to its original URL with low latency.
- Reject malformed URLs and support optional expiration and disablement.
- Assume redirects greatly outnumber URL creations; exact scale and retention
  requirements should be confirmed with the interviewer.

### API and data model

- `POST /api/links` accepts a URL and optional expiration/custom alias; returns
  the short URL and metadata.
- `GET /{code}` resolves a code and redirects to the destination.
- Store `{code, destination, created_at, expires_at, disabled}`. The code has
  a unique constraint so collisions cannot overwrite an existing mapping.

### Architecture and flow

Creation validates the scheme and destination, generates a random or
Base62-encoded identifier, then conditionally writes the mapping to a durable
key-value store. If the code already exists, generate another and retry.

Redirect first checks a cache, then reads the durable mapping on a miss. It
checks expiration and disabled status, populates the cache, and returns a 302
redirect. Unknown or expired codes return 404. Cache entries need a TTL no
longer than the mapping's remaining lifetime, and disable/delete operations
must invalidate or version cached entries.

### Tradeoffs, reliability, and security

- Random identifiers are simple and hard to enumerate but need collision
  retries; a sequence encoded as Base62 avoids collisions but reveals creation
  order and needs a distributed ID allocator.
- A cache reduces read latency and database load, at the cost of stale data.
  Durable storage remains the source of truth.
- Use replicated storage and backups for durability. Keep redirects available
  during cache or replica failures where possible, while failing creation if
  the durable write cannot be confirmed.
- Validate schemes, block private/internal network destinations if the
  service fetches URLs, rate-limit creation, and avoid exposing sequential IDs.
- Measure redirect latency, cache hit rate, creation errors, and unresolved
  codes. Add sharding or regional replicas only after traffic and latency
  targets justify them.

## Run

From this folder:

```bash
python day58.py
python -m pytest -q
```

The test for the broken implementation records the reproduced bug; the other
tests verify the corrected functions.