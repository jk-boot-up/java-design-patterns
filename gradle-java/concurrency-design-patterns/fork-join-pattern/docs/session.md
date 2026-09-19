# Session Guide — Fork-Join Pattern

A 60-minute session built around one question: how do you use every processor for one big job?

## Learning Objectives

1. Say what fork and join do.
2. Show the pieces running together.
3. Choose a threshold.
4. Say what limits the speedup.

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
cd concurrency-design-patterns/fork-join-pattern
./gradlew -q run
```

Act one: what was the total? Act two: how many pieces? Act three: how many at once? Act four: how many tasks for each threshold? Act five: what speedup did one big piece allow? Act six: how many ran when the work waited?

## Exercises

1. Try a threshold of 500 and count the pieces.
2. Change the costs so one piece is huge, and see the best speedup.
3. Replace the task with a parallel stream and compare the lines.

Close with the verdict: processor-bound work, an even split, a measured threshold, and a loop for small jobs.
