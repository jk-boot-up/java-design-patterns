# Session Guide — Splitter and Aggregator Pattern

A 60-minute session built around one question: how do you share one message between workers and put it back together?

## Learning Objectives

1. Say what each part carries.
2. Show parts arriving out of order and completing.
3. Show a timeout with a partial result.
4. Name the memory cost.

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
cd messaging-integration-patterns/splitter-aggregator-pattern
./gradlew -q run
```

Act one: how many steps in a row? Act two: what does each part carry? Act three: what order did they finish in? Act four: what order were the lines in the result? Act five: what was missing, and when did it give up? Act six: how many orders were held?

## Exercises

1. Make the aggregator reject a part whose total disagrees with the first it saw.
2. Add a limit on the number of open orders, and decide what to do at it.
3. Make the timeout a header, so urgent orders give up sooner.

Close with the verdict: number the parts, aggregate with a timeout, drop duplicates, and watch the open count.
