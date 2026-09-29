# Session Guide — Polling Consumer Pattern

## Learning Objectives

By the end of the session you can:

- Tell a polling consumer from an event-driven one.
- Let a consumer take only what it can handle.
- Pause and resume without losing messages.
- Choose a polling interval, and know what long polling is.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Pushed at the printer | 7 min |
| 0:17 | Act 2: A polling consumer | 7 min |
| 0:24 | Act 3: Pausing | 7 min |
| 0:31 | Act 4: How often to poll | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 40 refusals with act two's none.
Open `PollingConsumer.tick`: ask for up to five, print them. End on acts four
and five: how often would you poll in a real shop?

## Exercises

1. Poll faster when the last poll was full and slower when it was empty.
2. Print a warning when the queue holds more than 100 orders.
3. Rewrite the consumer with `BlockingQueue.poll(timeout)` for real long polling.
