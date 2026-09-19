# Session Guide — Retry with Resilience4j Pattern

A 60-minute session built around one question: what does Resilience4j give you for a retry, and what do you still decide?

## Learning Objectives

1. Read the retry's settings.
2. Explain why the exception list matters.
3. Explain why an idempotency key is needed.
4. Explain how retries multiply.

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
cd micro-services-design-patterns/retry-with-resilience4j-pattern
./gradlew -q run
```

Act one: how many calls did it take? Act two: what were the waits? Act three: what did the caller see at the end? Act four: which card was retried? Act five: how many charges were made? Act six: why nine calls?

## Exercises

1. Set the attempts to five and predict act six.
2. Remove the retry from the checkout layer and rerun act six.
3. Add a fallback method that returns a receipt for later.

Close with the verdict: temporary failures only, idempotency keys, one layer, small numbers.
