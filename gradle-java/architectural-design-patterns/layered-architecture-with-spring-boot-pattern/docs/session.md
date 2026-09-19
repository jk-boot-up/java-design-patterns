# Session Guide — Layered Architecture with Spring Boot Pattern

A 60-minute session built around one question: what does Spring Boot give a layered design, and what does it not check?

## Learning Objectives

1. Name the stereotype for each layer.
2. Say where the transaction belongs.
3. Explain why a test must enforce the rule.

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
cd architectural-design-patterns/layered-architecture-with-spring-boot-pattern
./gradlew -q run
```

Act one: which class handled the request? Act two: what did the rollback undo? Act three: where does a status number appear? Act four: what did Spring say about the shortcut? Act five: which field leaked? Act six: which tool found the shortcut?

## Exercises

1. Move the transaction to the controller and see what breaks.
2. Add a class that breaks the rule and run the test.
3. Add a field to the response and check nothing else leaks.

Close with the verdict: packages as layers, a transaction in the service, response objects, and a test.
