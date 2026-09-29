# Session Guide — Backpressure Pattern

## Learning Objectives

By the end of the session you can:

- Explain what happens when a producer outruns a consumer.
- Bound a buffer so the producer waits.
- Implement pull with `Flow.Subscription.request(n)`.
- Decide when dropping stale data is safe.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: No backpressure | 7 min |
| 0:17 | Act 2: A bounded buffer | 7 min |
| 0:24 | Act 3: Ask for what you can handle | 7 min |
| 0:31 | Act 4: Keep only the latest | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 9000 waiting with act two's 500.
Open `Indexer.onNext`: the next `request` is only made when a batch is done.
End on act four's 10 delivered out of 1000.

## Exercises

1. Replace `FeedSimulation`'s bounded buffer with a real `ArrayBlockingQueue` and two threads.
2. Use the JDK's `SubmissionPublisher` instead of `PullPublisher`.
3. Drop the oldest product when the buffer is full, instead of making the supplier wait.
