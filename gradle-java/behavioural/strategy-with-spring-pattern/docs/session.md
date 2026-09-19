# Session Guide — Strategy with Spring Pattern

A 60-minute session built around one question: how does Spring find and choose strategies?

## Learning Objectives

1. Say where the map's keys come from.
2. Explain why asking for the interface alone fails.
3. Explain why to check a configured name at startup.

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
cd behavioural/strategy-with-spring-pattern
./gradlew -q run
```

Act one: where did the keys come from? Act two: what does an unknown name do at run time? Act three: when is a wrong configured name found? Act four: why did four beans stop the start? Act five: which class changed when a rule was added? Act six: what did primary change?

## Exercises

1. Rename a bean and see which configuration breaks.
2. Add a sixth rule as a component and check the map.
3. Write a test that fails when a configured name is not a bean.

Close with the verdict: inject the map, name the beans, check at startup, primary for a default.
