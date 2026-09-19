# Session Guide — Rate Limiter Pattern

A 60-minute session built around one question: how does a service protect itself from a caller that asks too much?

## Learning Objectives

1. Say how a token bucket allows a burst and then a steady rate.
2. Explain why a bucket each is fairer.
3. Say what a refusal should tell the caller.
4. Name the three bills.

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
cd micro-services-design-patterns/rate-limiter-pattern
./gradlew -q run
```

Act one: how many requests beyond capacity? Act two: how many allowed in a burst of twenty? Act three: how many of the steady rate? Act four: who was refused with a shared bucket? Act five: what did the refusal say? Act six: how many allowed with three servers?

## Exercises

1. Make the bucket for a caller larger and see which polite requests stop being refused.
2. Add a cost to a request, so that a search takes three tokens.
3. Share one bucket between two servers through a small class, and count the difference.

Close with the verdict: a bucket per caller, a burst from real loads, an exact retry-after, and a shared count when exactness matters.
