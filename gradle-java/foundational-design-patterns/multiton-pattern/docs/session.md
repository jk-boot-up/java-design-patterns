# Session Guide — Multiton Pattern

A 60-minute session built around one question: how do you keep exactly one object for each key?

## Learning Objectives

1. Show copies of one warehouse disagreeing.
2. Show one per key.
3. Show a race making two, and the atomic fix.
4. Name the costs.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | The scenario and the naive version |
| 0:10–0:30 | The pattern |
| 0:30–0:45 | The bill |
| 0:45–0:52 | The verdict |
| 0:52–1:00 | Exercises |

## Walkthrough

```bash
cd foundational-design-patterns/multiton-pattern
./gradlew -q run
```

Act one: what stock did each copy have? Act two: how many were created? Act three: what stock did the other part see? Act four: what happened to Mars? Act five: how many were created without a lock? Act six: what stock did the next test see?

## Exercises

1. Add a fourth region.
2. Replace the set of regions with an enum.
3. Add a reset that tests call before each test.

Close with the verdict: exact key set, atomic create, resettable, or use an enum.
