# Session Guide — Special Case Pattern

## Learning Objectives

By the end of the session you can:

- Explain why null checks spread and why one missing check crashes.
- Write a special case that implements the ordinary interface.
- Tell a special case from an error.
- Tell Special Case from Null Object.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Null checks everywhere | 7 min |
| 0:17 | Act 2: A guest special case | 7 min |
| 0:24 | Act 3: An unknown customer | 7 min |
| 0:31 | Act 4: Behaviour, not type checks | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and open `Checkout.withNullChecks`: find the one line
without a check. Then open `SpecialCases`: two small records. Show that
`Checkout.run` has no `if` at all, and end on act five: when should a missing
account be an error instead?

## Exercises

1. Add a `Staff` special case with a 20% discount and no points.
2. Make `find` throw for IDs that do not match the pattern `C-` plus digits, so mistypes fail loudly.
3. Add a method `deliveryName()` and implement it for all three kinds of customer.
