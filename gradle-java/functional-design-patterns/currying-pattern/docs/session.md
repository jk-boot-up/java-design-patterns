# Session Guide — Currying Pattern

## Learning Objectives

By the end of the session you can:

- Define currying and partial application.
- Write a curried function in Java.
- Choose argument order for currying.
- Decide when a plain lambda is clearer.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Repeated arguments | 7 min |
| 0:17 | Act 2: A curried function | 7 min |
| 0:24 | Act 3: Ready-made functions | 7 min |
| 0:31 | Act 4: Argument order matters | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's three calls with act two's
`euStandard`. Open `Shipping.CURRIED`: one line of arrows. End on act four's
36.00 and 11.00.

## Exercises

1. Write a `curry3` helper for three-argument functions.
2. Build a `Map<Service, Function<Double, Double>>` for the UK.
3. Rewrite act three with plain lambdas and compare.
