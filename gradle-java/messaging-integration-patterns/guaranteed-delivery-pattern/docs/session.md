# Session Guide — Guaranteed Delivery Pattern

## Learning Objectives

By the end of the session you can:

- Explain why in-memory messages are lost on restart.
- Store before accepting; acknowledge after delivering.
- Replay unacknowledged messages after a crash.
- Explain at-least-once delivery and duplicates.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Only in memory | 7 min |
| 0:17 | Act 2: Written to disk first | 7 min |
| 0:24 | Act 3: Acknowledgements | 7 min |
| 0:31 | Act 4: At least once | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one. Open `Journal`: `send` and `acknowledge`
each append one forced line; `unacknowledged` reads the file and subtracts.
Open the journal file in `/tmp` to see the lines. End on act four.

## Exercises

1. Trim the journal: rewrite it without acknowledged messages when it passes 100 lines.
2. Make the email sender skip IDs it has already sent (an idempotent consumer).
3. Measure how much slower `send` is with `force(true)` than without.
