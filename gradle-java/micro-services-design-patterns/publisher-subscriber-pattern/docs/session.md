# Session Guide — Publisher-Subscriber Pattern

A 60-minute session built around one question: what does a topic let a publisher stop knowing, and what does it stop it knowing?

## Learning Objectives

1. Say what the publisher knows.
2. Show a subscriber added without a change.
3. Explain a backlog and a reader position.
4. Say why a late subscriber needs a kept log.

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
cd micro-services-design-patterns/publisher-subscriber-pattern
./gradlew -q run
```

Act one: how many services did the order service know? Act two: what changed to add loyalty? Act three: whose backlog was four? Act four: what did email receive? Act five: what did the live subscriber see? Act six: what was the publisher told?

## Exercises

1. Add a subscriber that only wants cancelled orders.
2. Make one subscriber's handler throw, and decide what the topic should do.
3. Limit the log to the last 100 events and see which late subscribers are hurt.

Close with the verdict: many independent parties, small past-tense events, a kept log, and subscribers safe to repeat.
