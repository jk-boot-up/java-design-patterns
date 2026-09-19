# Session Guide — MVC with Spring MVC Pattern

A 60-minute session built around one question: what does Spring MVC give the pattern, and where does it leak?

## Learning Objectives

1. Say what a controller returns.
2. Explain why the total is computed in the model.
3. Explain post, redirect, get.

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
cd architectural-design-patterns/mvc-with-spring-mvc-pattern
./gradlew -q run
```

Act one: which class named the view? Act two: which line chose JSON? Act three: how many times was the total computed? Act four: why did the totals differ? Act five: why did the one-line order fail? Act six: what does the redirect prevent?

## Exercises

1. Add a third view, a plain text summary.
2. Add a discount rule to the model and see both views change.
3. Move the sum out of the naive template and delete the template.

Close with the verdict: model computes, view shows, controller connects.
