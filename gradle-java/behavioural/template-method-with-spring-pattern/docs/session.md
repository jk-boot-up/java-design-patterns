# Session Guide — Template Method with Spring Pattern

A 60-minute session built around one question: what does a Spring template own, and what does it decide for you?

## Learning Objectives

1. Explain which steps the template owns.
2. Say why plain JDBC can leak a connection.
3. Name two decisions the template makes silently.

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
cd behavioural/template-method-with-spring-pattern
./gradlew -q run
```

Act one: which line leaked? Act two: which line stopped the leak? Act three: which line was ours? Act four: which exception did each catch? Act five: what does a missing row do? Act six: what did the rollback undo?

## Exercises

1. Add try-with-resources to the by-hand method and rerun act one.
2. Add a query that returns an Optional instead of throwing.
3. Make the reserve step fail first, and see what the transaction undoes.

Close with the verdict: the template, its silent decisions, small lambdas, translated exceptions.
