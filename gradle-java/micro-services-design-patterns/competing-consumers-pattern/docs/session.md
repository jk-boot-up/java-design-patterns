# Session Guide — Competing Consumers Pattern

A 60-minute session built around one question: how do several workers share one queue safely?

## Learning Objectives

1. Say what the broker guarantees.
2. Show ordering lost.
3. Show a failed message taken over.
4. Show the duplicate and its fix.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | The scenario and the naive version |
| 0:10–0:30 | The pattern |
| 0:30–0:45 | The bill |
| 0:45–0:52 | The verdict |
| 0:52–1:00 | Exercises |

## Walkthrough

```bash
cd micro-services-design-patterns/competing-consumers-pattern
./gradlew -q run
```

Act one: how many in progress with three consumers? Act two: how many different orders? Act three: in what order did they finish? Act four: which attempt succeeded? Act five: how many charges, and how many with a memory? Act six: how many were waiting?

## Exercises

1. Make the consumer safe to run twice, and prove it by delivering every message twice.
2. Partition the queue by customer, so one customer's orders stay in order.
3. Add a limit on redeliveries and a place for messages that keep failing.

Close with the verdict: independent work, acknowledge when done, safe to repeat, and sized for the shared limit.
