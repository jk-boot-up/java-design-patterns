# Session Guide — Event-Driven Architecture Pattern

A 60-minute session built around one question: what does a log let services stop depending on, and what does it cost?

## Learning Objectives

1. Show an order lost by a direct call.
2. Show a down service that catches up.
3. Show a new reader added with no change to the writer.
4. Explain eventual consistency and duplicates.

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
cd architectural-design-patterns/event-driven-architecture-pattern
./gradlew -q run
```

Act one: was the order accepted? Act two: what did the order service know? Act three: how far behind was shipping? Act four: what did analytics see? Act five: what was the stock at first? Act six: what was the stock without a check?

## Exercises

1. Add a shipping reader that fails on one event.
2. Add an event for a cancelled order, and undo the stock.
3. Add a lag report for every reader.

Close with the verdict: write facts, read at your own pace, keep the log, expect delay, be safe to repeat.
