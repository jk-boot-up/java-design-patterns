# Session Guide — Strangler Fig Pattern

A 60-minute session built around one question: how do you replace a system that must keep running?

## Learning Objectives

1. Explain why a big-bang rewrite has an all-or-nothing rollback.
2. Explain a router with a switch per capability.
3. Explain what shadow reads catch and why they come before a move.
4. Say why a stalled migration is worse than either endpoint.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the big bang |
| 0:10–0:22 | The router |
| 0:22–0:38 | Shadow reads |
| 0:38–0:50 | Rollback and the bill |
| 0:50–1:00 | The stall, and the verdict |

## Walkthrough

```bash
cd platform-design-patterns/strangler-fig-pattern
./gradlew -q run
```

Act one: what is the smallest unit you can roll back? Act two: which capability would you move first? Act three: read the first shadow difference. Act four: what did not move back? Act five: which table is the truth? Act six: who owns the end date?

## Exercises

1. Move stock next, and decide how to keep its two tables in step.
2. Add a fifth capability, and count what changes.
3. Change the cost model so the both-live overhead is 10. Does stalling stop being worse?

Close with the verdict: finish it, or do not start.
