# Session Guide — Remote Facade Pattern

## Learning Objectives

By the end of the session you can:

- Explain why chatty remote calls are slow.
- Design a coarse call around what a screen needs.
- Make a remote change all or nothing.
- Keep business rules out of the facade.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Many small remote calls | 7 min |
| 0:17 | Act 2: One facade call | 7 min |
| 0:24 | Act 3: A change in one call | 7 min |
| 0:31 | Act 4: Fine-grained inside | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare the round trips in acts one and two. Open
`FineGrainedApi` and `OrderFacade` side by side. Spend time on act three: the
half-changed order is the bug learners will meet in real APIs.

## Exercises

1. Add a `/order-summary?fields=slot` option. What have you started building?
2. Add a cancel action to the facade that refuses if the order has shipped.
3. Count round trips for a list screen of 20 orders, with small calls and with a facade.
