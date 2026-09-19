# Session Guide — Event-Driven Architecture with Kafka Pattern

A 60-minute session built around one question: what does a real broker keep for you, and what must every reader still do?

## Learning Objectives

1. Say what the broker remembers.
2. Show a reader catching up from its offset.
3. Show a new reader replaying history.
4. Say why readers must be safe to repeat.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:25 | The first acts |
| 0:25–0:40 | The failures of its own |
| 0:40–0:52 | The cost |
| 0:52–1:00 | Exercises and the verdict |

## Walkthrough

```bash
cd architectural-design-patterns/event-driven-architecture-with-kafka-pattern
./gradlew -q run
```

Act one: was the order accepted? Act two: what offset did the event get? Act three: how far behind was shipping? Act four: what did analytics see? Act five: what was the stock at first? Act six: what was the stock without a check?

## Exercises

1. Add a loyalty reader that reads from the start.
2. Make a reader fail before it commits, and see what it reads next.
3. Add a second partition, and think about what order means.

Close with the verdict: a group for each service, readers behind by design, safe to repeat, and watch the lag.
