# Session Guide — Queue-Based Load Leveling Pattern

A 60-minute session built around one question: what does a queue do for a service that meets a burst, and what does it cost?

## Learning Objectives

1. Say what a queue does to a burst.
2. Show the wait it costs.
3. Explain why an unbounded queue is dangerous.
4. Say what must be true of a queue that holds orders.

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
cd micro-services-design-patterns/queue-based-load-leveling-pattern
./gradlew -q run
```

Act one: how many refused without a queue? Act two: how deep did the queue get? Act three: how long did the last order wait? Act four: what did the unbounded queue reach? Act five: what did doubling the worker do? Act six: how many were lost?

## Exercises

1. Change the queue limit to 200 and rerun act four.
2. Add a second worker and compare it with doubling the first.
3. Add a priority for orders over one hundred pounds.

Close with the verdict: a bounded, durable queue, a worker sized for the average, and a watch on the depth.
