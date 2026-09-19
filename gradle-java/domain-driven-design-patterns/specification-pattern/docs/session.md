# Session Guide — Specification Pattern

A 60-minute session built around one question: what does a specification give a business rule that an if statement does not?

## Learning Objectives

1. Show how three copies of a rule drift.
2. Build a new rule from small ones.
3. Say how a rule explains itself.
4. Say what the in-memory bill is.

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
cd domain-driven-design-patterns/specification-pattern
./gradlew -q run
```

Act one: which copy drifted, and how? Act two: where was the rule named? Act three: which rules were combined? Act four: which part did each product fail? Act five: which two jobs did one rule do? Act six: how many products were looked at?

## Exercises

1. Add a rule for products in a given category that are also on sale, from existing small rules.
2. Add a `xor` to Specification and test it against its truth table.
3. Turn one specification into an SQL where clause, by hand.

Close with the verdict: shared, combined or self-explaining rules, small leaves, and a lambda when it is used once.
