# Session Guide — Resequencer Pattern

## Learning Objectives

By the end of the session you can:

- Explain why messages arrive out of order.
- Resequence by a sequence number per key.
- Handle a gap that never fills.
- Say when ordering can be avoided instead.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Applied as they arrive | 7 min |
| 0:17 | Act 2: A resequencer | 7 min |
| 0:24 | Act 3: Hold and release | 7 min |
| 0:31 | Act 4: One sequence per order | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one's statuses aloud. Open
`Resequencer.accept` and `release`: a buffer per order and a next-expected
number. End on act five: what should a real shop show for the missing PACKED?

## Exercises

1. Give up on a gap after 2 seconds instead of after 2 held messages.
2. When a gap is skipped, log which numbers were missed.
3. Ignore any update with a number already released (a duplicate).
