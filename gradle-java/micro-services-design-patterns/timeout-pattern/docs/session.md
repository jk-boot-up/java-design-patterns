# Session Guide — Timeout Pattern

A 60-minute session built around one question: what does a timeout protect you from, and what does it not tell you?

## Learning Objectives

1. Say what a call with no limit costs.
2. Explain why giving up does not stop the work.
3. Choose a limit from a spread of latencies.
4. Share a budget across a chain.

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
cd micro-services-design-patterns/timeout-pattern
./gradlew -q run
```

Act one: what state was the thread in? Act two: what did the page show? Act three: how many calls finished at the supplier after the caller gave up? Act four: how many succeeded at each limit? Act five: which call was cut off? Act six: what did the customer think, and what was true?

## Exercises

1. Change the budget to two seconds and see which calls are cut off.
2. Add a timeout to the payment call and an idempotency key, and retry safely.
3. Measure real latencies and choose a limit from the ninety-ninth percentile.

Close with the verdict: a timeout everywhere, chosen from real latencies, budgets for chains, and operations that are safe to ask about again.
