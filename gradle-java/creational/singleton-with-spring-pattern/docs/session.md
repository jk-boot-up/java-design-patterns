# Session Guide — Singleton with Spring Pattern

A 60-minute session built around one question: what does a Spring singleton guarantee, and what does it not?

## Learning Objectives

1. Explain that the scope is per container.
2. Name the ways to get a second instance.
3. Explain why shared state needs its own thread safety.

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
cd creational/singleton-with-spring-pattern
./gradlew -q run
```

Act one: who holds the generator? Act two: why did new work? Act three: how many containers ran? Act four: what changed in the bean definition? Act five: when was it built? Act six: which line makes it safe?

## Exercises

1. Make the constructor private and see what Spring does.
2. Make the demo's second context share the first one's bean.
3. Replace the AtomicLong with a plain long and rerun a threaded test.

Close with the verdict: one container, thread-safe state, and an enum when no container is around.
