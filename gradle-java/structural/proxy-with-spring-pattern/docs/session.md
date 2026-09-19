# Session Guide — Proxy with Spring Pattern

A 60-minute session built around one question: what does Spring's generated proxy cover, and what slips past it?

## Learning Objectives

1. Say that the bean is a generated subclass.
2. Explain why a call on `this` skips the rule.
3. Explain why a final method is not covered.

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
cd structural/proxy-with-spring-pattern
./gradlew -q run
```

Act one: what class is the bean? Act two: which line refuses the shopper? Act three: when was the image loaded? Act four: how many places hold the rule? Act five: why did the shopper get the image? Act six: what did the final method see?

## Exercises

1. Fix act five by injecting the bean into itself, and test it.
2. Add a second aspect that counts calls, and order the two.
3. Remove `final` from `renderFinal` and rerun act six.

Close with the verdict: one aspect per rule, calls from outside, no final methods.
