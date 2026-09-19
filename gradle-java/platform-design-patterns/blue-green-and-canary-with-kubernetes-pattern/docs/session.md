# Session Guide — Blue-Green and Canary with Kubernetes Pattern

A 60-minute session built around one question: what does a real cluster add to blue-green and canary?

## Learning Objectives

1. Say what the Service selector does.
2. Explain why a new connection is needed for each request.
3. Say what a canary's spread depends on.
4. Name the cost of two releases running.

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
cd platform-design-patterns/blue-green-and-canary-with-kubernetes-pattern
./gradlew -q run
```

Act one: how many requests failed in the gap? Act two: what did the switch change? Act three: what did going back cost? Act four: what share reached v2? Act five: did the gate halt it? Act six: how many pods ran?

## Exercises

1. Change the gate to two failures in a hundred.
2. Add a third release, v3, and switch to it.
3. Make v2 slow instead of failing, and think about what the gate should watch.

Close with the verdict: beside not on top, switch by selector, canary by replicas, gate on failures.
