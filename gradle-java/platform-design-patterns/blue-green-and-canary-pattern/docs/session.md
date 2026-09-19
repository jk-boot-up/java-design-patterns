# Session Guide — Blue-Green and Canary Pattern

A 60-minute session built around one question: how can a release go live with the smallest risk to customers?

## Learning Objectives

1. Show the failures of an in-place upgrade.
2. Show a switch and a switch back.
3. Show a canary meeting few failures.
4. Explain the gate, and the data problem.

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
cd platform-design-patterns/blue-green-and-canary-pattern
./gradlew -q run
```

Act one: how many failed? Act two: how many failed with a good switch? Act three: what happened after going back? Act four: how many failed with a canary? Act five: which release was halted? Act six: what could v1 not read?

## Exercises

1. Change the gate to two percent.
2. Make v2 fail on orders over fifty pounds, and see the canary catch it.
3. Make v1 able to read v2's format.

Close with the verdict: beside, not on top; switch by a setting; canary for risk; keep data compatible.
