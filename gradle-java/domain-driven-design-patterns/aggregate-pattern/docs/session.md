# Session Guide — Aggregate Pattern

A 60-minute session built around one question: what is an aggregate for, and how big should it be?

## Learning Objectives

1. Say what a root is, and why lines cannot be built outside it.
2. Explain why other aggregates are held by id.
3. Explain what a version check protects.
4. Say what happens when an aggregate is too big.

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
cd domain-driven-design-patterns/aggregate-pattern
./gradlew -q run
```

Act one: which rules did the loose order break? Act two: which line names the rule? Act three: what stops a line being built outside? Act four: how many customer loads? Act five: which clerk was refused? Act six: what did the wide boundary cost?

## Exercises

1. Add a rule that an order can hold at most five different items.
2. Add a `removeLine` method and keep every rule true.
3. Add a Customer aggregate with its own id and its own rules.

Close with the verdict: one root, the rules inside it, other aggregates by id, and a boundary no wider than it needs to be.
