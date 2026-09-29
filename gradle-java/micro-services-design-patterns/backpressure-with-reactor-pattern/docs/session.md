# Session Guide — Backpressure with Project Reactor Pattern

## Learning Objectives

By the end of the session you can:

- Explain demand in Reactive Streams.
- Request items in batches with a BaseSubscriber.
- Use `limitRate` and read its request pattern.
- Choose between buffer, drop and latest.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A source that ignores demand | 7 min |
| 0:17 | Act 2: Produce only what is asked | 7 min |
| 0:24 | Act 3: limitRate | 7 min |
| 0:31 | Act 4: Only the latest | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Compare act one's OverflowException with act two's
steady ten at a time. Read act three's requests. End on act four's two values.

## Exercises

1. Replace IGNORE in act one with BUFFER and watch memory instead of an error.
2. Use `onBackpressureDrop` in act four and print what is dropped.
3. Build the feed with `Flux.generate` so it only produces on demand.
