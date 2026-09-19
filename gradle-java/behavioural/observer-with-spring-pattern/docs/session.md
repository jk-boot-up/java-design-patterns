# Session Guide — Observer with Spring Pattern

A 60-minute session built around one question: how does delivery really behave in Spring's events?

## Learning Objectives

1. Explain that delivery is synchronous.
2. Explain what a failing listener does to the others.
3. Explain why a missing listener is silent.

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
cd behavioural/observer-with-spring-pattern
./gradlew -q run
```

Act one: what does the order hold? Act two: which thread ran the listeners? Act three: who heard about the failed order? Act four: when did the audit run? Act five: which condition selected the events? Act six: how many listeners ran?

## Exercises

1. Wrap the email listener's body in a try block and see act three change.
2. Make the analytics listener asynchronous.
3. Publish an event with a typo in its class name and see what changes.

Close with the verdict: publish events, isolate failures, choose threads, and test the wiring.
