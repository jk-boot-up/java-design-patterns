# Session Guide — Hedged Requests Pattern

## Learning Objectives

By the end of the session you can:

- Explain tail latency and why the median hides it.
- Choose a hedge delay near the normal worst case.
- Race two calls and cancel the loser.
- Decide which calls may be hedged.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One call, and a slow tail | 7 min |
| 0:17 | Act 2: Hedge after 50 ms | 7 min |
| 0:24 | Act 3: Hedge at once | 7 min |
| 0:31 | Act 4: A real race | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 1000 ms with act two's 70 ms. Open
`Hedger.call`: submit, poll with a timeout, submit again, take the first,
cancel the other. End on act three's 100% extra calls.

## Exercises

1. Rewrite `Hedger` with `CompletableFuture.anyOf` and `orTimeout`.
2. Add a budget: stop hedging once hedges exceed 5% of recent calls.
3. Try hedge delays of 10, 50 and 200 ms and compare the tail and the load.
