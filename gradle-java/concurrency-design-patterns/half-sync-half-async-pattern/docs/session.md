# Session Guide — Half-Sync/Half-Async Pattern

## Learning Objectives

By the end of the session you can:

- Explain why an event thread must never block.
- Separate accepting from processing with a queue.
- Write plain blocking workers for the sync half.
- Choose a queue limit and a full-queue policy.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Blocking work on the event thread | 7 min |
| 0:17 | Act 2: The async half | 7 min |
| 0:24 | Act 3: The sync half | 7 min |
| 0:31 | Act 4: The queue absorbs the burst | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's acceptance delay with act two's.
Open `HalfSyncHalfAsync`: `burst` is the async half, `workLoop` the sync half,
and the `ArrayBlockingQueue` joins them. End on act five and ask what a real
shop should do with the orders it turned away.

## Exercises

1. Instead of turning orders away, save them to a file and retry later.
2. Change the number of workers from 4 to 1 and 8. What happens to the total time?
3. Replace the worker threads with virtual threads. What changes, and what stays?
