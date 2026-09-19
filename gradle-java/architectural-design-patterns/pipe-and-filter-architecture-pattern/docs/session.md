# Session Guide — Pipe and Filter Architecture Pattern

A 60-minute session built around one question: what sets the speed of a pipeline, and how do you speed it up?

## Learning Objectives

1. Compare one big step with three stages.
2. Find the slowest stage from the queue sizes.
3. Widen only that stage.
4. Explain backpressure.

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
cd architectural-design-patterns/pipe-and-filter-architecture-pattern
./gradlew -q run
```

Act one: how many orders finished? Act two: how many now? Act three: which line was longest? Act four: what became the limit? Act five: how many were refused? Act six: how many orders were lost?

## Exercises

1. Make parse take two ticks and find the new slowest stage.
2. Give pack two workers and see whether anything changes.
3. Keep the lines in a list that survives a crash.

Close with the verdict: find the slow stage, widen it alone, limit the lines, and keep them if the orders matter.
