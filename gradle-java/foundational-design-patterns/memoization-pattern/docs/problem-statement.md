# Problem Statement

## The scenario

The store works out multi-buy prices recursively and asks the carrier for
shipping quotes on every product page view.

## The naive version

The plain recursion recomputes the same smaller answers (9,749,473 calls for
25 mugs), and every page view waits 200 ms for a quote it has already had.

## What this project must deliver

- The call count of the plain recursion, and of the memoized one (26).
- A reusable `Memo` wrapper cutting 1000 quotes to 12.
- A stale answer from memoizing a function that depends on the time.
- Unbounded growth shown: 100,000 entries.
- Every printed result asserted by a test.
