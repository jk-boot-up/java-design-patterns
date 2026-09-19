# Session Guide — Scatter-Gather Pattern

A 60-minute session built around one question: how do you ask many at once without waiting for the slowest?

## Learning Objectives

1. Compare in turn, at once and with a deadline.
2. Show a partial result named honestly.
3. Show a failure treated as a late answer.
4. Name the cost of fan-out.

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
cd micro-services-design-patterns/scatter-gather-pattern
./gradlew -q run
```

Act one: what was the total in turn? Act two: what was it together? Act three: which supplier was left out? Act four: what would the left-out price have been? Act five: which supplier failed? Act six: how many calls for a thousand views?

## Exercises

1. Add a fifth supplier that is always slow, and see what the deadline does.
2. Return the answers as they arrive, without waiting for the deadline.
3. Cache each supplier's price for a minute, and count the calls again.

Close with the verdict: a deadline always, failure as lateness, partial answers named, and fan-out watched.
