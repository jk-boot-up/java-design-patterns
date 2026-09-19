# Session Guide — Onion Architecture Pattern

A 60-minute session built around one question: what should the business rules depend on, and what should depend on them?

## Learning Objectives

1. Name the rings and the one rule.
2. Show a checker catching an outward reference.
3. Show storage swapped without touching the inside.
4. Show the rules checked with no storage.

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
cd architectural-design-patterns/onion-architecture-pattern
./gradlew -q run
```

Act one: what did the order call? Act two: how many violations? Act three: which class broke the rule? Act four: which parts were untouched? Act five: what was used to check the rules? Act six: how many conversions?

## Exercises

1. Add a third storage and run the checker.
2. Add a rule for free delivery, in ring one.
3. Add an outward reference on purpose, and see the checker name it.

Close with the verdict: rules at the centre, dependencies inward, checked by a test.
