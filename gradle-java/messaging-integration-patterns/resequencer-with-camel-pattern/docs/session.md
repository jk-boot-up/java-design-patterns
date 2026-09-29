# Session Guide — Resequencer with Apache Camel Pattern

## Learning Objectives

By the end of the session you can:

- Use `resequence()` in stream and batch modes.
- Explain the first-message delay of stream mode.
- Keep several sequences apart with batch mode.
- Choose a timeout for lost messages.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Applied as they arrive | 7 min |
| 0:17 | Act 2: Stream mode | 7 min |
| 0:24 | Act 3: Batch mode | 7 min |
| 0:31 | Act 4: Two orders at once | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Compare acts two and three: the same updates, released
as a stream and as a batch. Open `ShopRoutes`: each mode is one line. End on
act five's half-second wait.

## Exercises

1. Set the stream timeout to 2 seconds and time how long the page stays on PAID.
2. Add `rejectOld()` and send #2 again after #4 has been released.
3. Give each order its own route so stream mode can keep per-order sequences.
