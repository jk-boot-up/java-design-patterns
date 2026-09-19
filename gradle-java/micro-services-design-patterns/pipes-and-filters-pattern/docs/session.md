# Session Guide — Pipes and Filters Pattern

A 60-minute session built around one question: what does breaking a job into filters give you, and what does it cost?

## Learning Objectives

1. Say what a filter is.
2. Swap and add a step without changing another.
3. Report rejects with their reason.
4. Explain streaming and its memory.

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
cd micro-services-design-patterns/pipes-and-filters-pattern
./gradlew -q run
```

Act one: how many jobs in the loop? Act two: which step ran alone? Act three: what changed when the tax step was swapped? Act four: which lines were rejected, and why? Act five: how many items were held in each mode? Act six: what failed with loose maps?

## Exercises

1. Add a step that removes duplicate customers, and see what it needs to hold.
2. Add a step that adds a delivery charge for orders under fifty pounds.
3. Make the pipeline stop after ten rejects.

Close with the verdict: small typed steps, reasons for rejects, streaming for size, and a short pipeline.
