# Session Guide — Circuit Breaker with Resilience4j Pattern

A 60-minute session built around one question: what does Resilience4j give you for a circuit breaker, and what can go wrong?

## Learning Objectives

1. Read the breaker's settings.
2. Explain why the fallback hides failures.
3. Explain why a call on `this` bypasses the breaker.

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
cd micro-services-design-patterns/circuit-breaker-with-resilience4j-pattern
./gradlew -q run
```

Act one: what is the window? Act two: which call opened it? Act three: how many calls reached the service? Act four: what did the probe decide? Act five: which exception was ignored? Act six: why did the breaker see nothing?

## Exercises

1. Change the window to six and predict act two.
2. Remove the ignore list and rerun act five.
3. Move the call in act six to another bean and rerun it.

Close with the verdict: configure on purpose, ignore client errors, alert on state, call from outside.
