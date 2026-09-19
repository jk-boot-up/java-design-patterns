# Session Guide — Transaction Script Pattern

A 60-minute session built around one question: when is one procedure enough, and how do you notice it is not?

## Learning Objectives

1. Say what a transaction script is and why it is one transaction.
2. Show how copied rules drift.
3. Count the growth of decisions.
4. Name where a script is best.

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
cd enterprise-design-patterns/transaction-script-pattern
./gradlew -q run
```

Act one: which method does everything? Act two: what was undone? Act three: which script was not told? Act four: which function did they share? Act five: how many paths, before and after? Act six: what is a script best at?

## Exercises

1. Add a fourth rule to the grown script and count the new paths.
2. Move the loyalty rule into a helper and see what it changes.
3. Write the same order placement as a set of objects and compare the length.

Close with the verdict: scripts for simple, sequential logic, helpers for shared rules, and a move to a domain model when rules multiply.
