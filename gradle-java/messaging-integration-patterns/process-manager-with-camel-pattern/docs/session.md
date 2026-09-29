# Session Guide — Process Manager with Apache Camel Pattern

## Learning Objectives

By the end of the session you can:

- Start a saga with completion and compensation routes.
- Let a step join the saga and name its own compensation.
- Trace what Camel calls when a later step fails.
- Explain why production needs a durable coordinator.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Steps hand on to each other | 7 min |
| 0:17 | Act 2: A saga | 7 min |
| 0:24 | Act 3: A branch | 7 min |
| 0:31 | Act 4: Camel runs the undo steps | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Compare act one's 1 of 3 kettles with act four's 2 of 3.
Open `ShopRoutes`: the saga is four lines, the reserve step's compensation
two more. End on act five's costs.

## Exercises

1. Add a compensation to shipping that books a return label.
2. Make shipping fail for one order and trace every compensation called.
3. Replace InMemorySagaService with Camel's LRA saga service and a coordinator.
