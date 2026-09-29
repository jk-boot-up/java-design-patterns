# Session Guide — Proactor Pattern

## Learning Objectives

By the end of the session you can:

- Explain initiating an operation versus waiting for it.
- Write completed and failed handlers.
- Chain handlers for connect, write and read.
- Compare Proactor with Reactor.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One after another | 7 min |
| 0:17 | Act 2: Start everything at once | 7 min |
| 0:24 | Act 3: Completion handlers | 7 min |
| 0:31 | Act 4: A failure is a completion | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare the times in acts one and two. Open
`ProactorQuotes`: `start` only starts. Follow one request through
`Connected`, `Written` and `Read`. End with act four: the failure path is a
handler too.

## Exercises

1. Add a timeout: a supplier that takes more than 0.5 s counts as failed.
2. Rewrite `ProactorQuotes` with `HttpClient.sendAsync` and `CompletableFuture`. What disappears?
3. Rewrite `BlockingQuotes` with one virtual thread per supplier. Compare the time and the code.
