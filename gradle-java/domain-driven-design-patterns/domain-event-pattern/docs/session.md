# Session Guide — Domain Event Pattern

A 60-minute session built around one question: what does a domain event let an order stop knowing, and what does it cost?

## Learning Objectives

1. Say why an event is a record in the past tense.
2. Explain what a failing handler does to the order.
3. Explain the gap between saving and telling.
4. Say what a handler must be safe against.

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
cd domain-driven-design-patterns/domain-event-pattern
./gradlew -q run
```

Act one: what state was left half done? Act two: which line called nobody? Act three: when did the reactions happen? Act four: which reaction was retried, and how many times? Act five: in what order were the events? Act six: what was kept across the stop?

## Exercises

1. Add an OrderShipped event and a handler that reacts to it.
2. Make the email handler safe to run twice.
3. Add a second relay run and check nothing is delivered twice.

Close with the verdict: past-tense facts, saved with the aggregate, delivered separately, handlers safe to repeat.
