# Session Guide — Higher-Order Functions Pattern

## Learning Objectives

By the end of the session you can:

- Define a higher-order function.
- Pass behaviour into a method as a `Predicate`.
- Return functions from functions, and combine them.
- Compose functions and explain why order matters.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A loop for every question | 7 min |
| 0:17 | Act 2: Pass the test in | 7 min |
| 0:24 | Act 3: Functions that make functions | 7 min |
| 0:31 | Act 4: Price rules as values | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's three loops with act two's one.
Open `Catalogue`: `filter` takes a function, `priceBelow` returns one. End on
act four's 31.00 and 32.00.

## Exercises

1. Add `priceBetween(low, high)` using `priceBelow` and `negate`.
2. Rewrite `filter` with `stream().filter(...)`.
3. Add a price rule that rounds to the nearest .99.
