# Session Guide — Hexagonal Architecture with Spring Boot Pattern

A 60-minute session built around one question: how does Spring wire a hexagon, and what keeps it a hexagon?

## Learning Objectives

1. Say where the core meets the container.
2. Explain how a property chooses an adapter.
3. Explain why a rule must guard the core.

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
cd architectural-design-patterns/hexagonal-architecture-with-spring-boot-pattern
./gradlew -q run
```

Act one: what class was the use case? Act two: what changed with the property? Act three: which two doors were used? Act four: how was the core run with no container? Act five: which class broke the rule? Act six: when was the missing adapter found?

## Exercises

1. Add a third storage adapter and choose it by property.
2. Add an annotation to the core and run the rule.
3. Add a REST driving adapter.

Close with the verdict: plain core, one config class, adapters by property, and a rule.
