# Session Guide — Unit of Work Pattern

A 60-minute session built around one question: what should happen to the first two writes when the third fails?

## Learning Objectives

1. Describe the wreckage when objects save themselves.
2. Say what a transaction fixes and what it costs.
3. Explain what a unit of work registers, and when it writes.
4. Explain why write order matters.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the wreckage |
| 0:10–0:22 | The transaction, and its cost |
| 0:22–0:36 | The pattern |
| 0:36–0:50 | The bill |
| 0:50–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/unit-of-work-pattern
./gradlew -q run
```

Act one: count what survived. Act two: why is 22 ticks a problem? Act three: how many operations happened before commit? Act four: what state is the database in? Act five: which table must be written first, and why? Act six: which is right, memory or the database?

## Exercises

1. Add `registerRemoved` to the placement and cancel an order.
2. Make the unit of work detect dirty objects itself by comparing snapshots.
3. Add a fourth product and a fourth line. How many changes are registered?

Close with: do the slow work first, then write everything once.
