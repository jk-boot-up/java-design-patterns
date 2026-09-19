# Session Guide — Serverless Pattern

A 60-minute session built around one question: when is it cheaper to pay per call than to keep a machine on?

## Learning Objectives

1. Compare an idle server with a function per event.
2. Show scaling out and back to zero.
3. Show a cold start and lost memory.
4. Find where pay per call stops being cheaper.

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
cd architectural-design-patterns/serverless-pattern
./gradlew -q run
```

Act one: what was the server's bill? Act two: what was the function bill? Act three: how many instances at once? Act four: how long was the cold start? Act five: what did the instance remember afterwards? Act six: which was dearer when busy?

## Exercises

1. Find the number of calls where functions and the server cost the same.
2. Give the platform two extra warm instances and see the cold starts drop.
3. Keep the count in a store, not the instance.

Close with the verdict: short, bursty, no memory, state outside, and price it at your busiest.
