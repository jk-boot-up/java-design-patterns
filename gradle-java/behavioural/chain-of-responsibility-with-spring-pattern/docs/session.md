# Session Guide — Chain of Responsibility with Spring Pattern

A 60-minute session built around one question: what does Spring give you for a chain, and what does it hide?

## Learning Objectives

1. Say where the order comes from.
2. Explain why order changes cost.
3. Explain what happens when a link throws.

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
cd behavioural/chain-of-responsibility-with-spring-pattern
./gradlew -q run
```

Act one: where does the order come from? Act two: which links never ran? Act three: how many paid calls in each order? Act four: what did the chain do with the exception? Act five: what did the property remove? Act six: who answered when nobody did?

## Exercises

1. Give two checks the same order number and see what happens.
2. Add a link and predict its position.
3. Make a link throw a checked exception.

Close with the verdict: cheap first, a policy for a throwing link, print the order, test the whole chain.
