# Session Guide — Lenses for Immutable Updates Pattern

## Learning Objectives

By the end of the session you can:

- Explain the cost of nested immutable updates.
- Write a lens as a getter and a setter.
- Join lenses to reach deep fields.
- State the three lens laws.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Rebuilding by hand | 7 min |
| 0:17 | Act 2: One lens | 7 min |
| 0:24 | Act 3: Lenses join | 7 min |
| 0:31 | Act 4: Change with a function | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's swapped address with act three's
one-line update. Open `Lens.andThen`: get through, set back out. End with
`LensLawsTest`.

## Exercises

1. Add a `CUSTOMER_NAME` lens and an `ORDER_CUSTOMER_NAME` lens.
2. Write a lens for the first order line.
3. Compare with a `withPostcode` method on each record.
