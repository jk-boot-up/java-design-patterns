# Session Guide — Fluent Interface Pattern

A 60-minute session built around one question: what makes a chain of calls easier to read than a list of arguments, and what does it cost?

## Learning Objectives

1. Show swapped arguments that compile.
2. Show the same call as a sentence.
3. Show the danger of a query that changes itself.
4. Show guided steps.

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
cd foundational-design-patterns/fluent-interface-pattern
./gradlew -q run
```

Act one: what changed when the booleans swapped? Act two: what did the sentence return? Act three: which call needed no order? Act four: what did cheap return in each version? Act five: what was offered first? Act six: where was the mistake found?

## Exercises

1. Add a call for a category filter.
2. Check the price limit in under(), not in run().
3. Add a step that must come before inStock.

Close with the verdict: never-changing calls, early checks, staged types for order, and a small surface.
