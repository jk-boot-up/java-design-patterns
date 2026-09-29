# Memoization, Explained

## The pattern in one sentence

Memoization remembers the answer a function gave for each argument and
returns it again instead of recomputing, which is correct only when the answer
depends on nothing but the argument.

## The 5 acts

### 1. The same questions again

`MultiBuy.plain` works out the best price for n mugs as the cheapest of: one
offer, plus the best price for what is left. That is correct, and the answer
for 25 mugs is £75.00. But "best for 20 mugs" is worked out again every time
any path reaches it, and the method is called 9,749,473 times.

### 2. Memoized

`MultiBuy.memoized` is the same code, with one change: before working out the
answer for n, it looks in a map; after working it out, it stores it. Each size
from 0 to 25 is worked out exactly once: 26 calls, the same £75.00.

### 3. A reusable memo

`Memo` wraps any function with `computeIfAbsent`. Wrapped around the carrier's
shipping quote, 1000 product page views spread over 12 postcode areas make only
12 slow calls: 2.4 seconds of waiting instead of 200.

### 4. Not safe to memoize

Converting pounds to euros depends on the day's rate, not only on the price. A
memo stores £100.00 as €116.00 in the morning. At noon the rate changes; the
real price is now €112.00, but the memo still answers €116.00.

### 5. The bill

A memo never forgets. Asked for 100,000 different postcodes, it keeps 100,000
answers. Real caching libraries add a size limit and an expiry time, which is
the difference between a memo and a cache.

## The verdict

Memoize expensive, pure functions that are asked the same questions again,
especially recursive ones. For anything that can go out of date or has many
distinct arguments, use a cache with expiry and a size limit.

## How to recognise this in code you did not write

- `Map.computeIfAbsent` around an expensive call.
- A `memo`, `cache` or `seen` map next to a recursive method.
- `@Cacheable`, `useMemo`, `functools.lru_cache`.

## Where you have already met this

- `Map.computeIfAbsent`, the one-line way to memoize in Java.
- Dynamic programming in algorithm courses, which is memoization of recursive problems.
- Caching libraries such as Caffeine, which add size limits and expiry.
- `useMemo` in React, and `@Cacheable` in Spring.
