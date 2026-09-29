# Session Guide — Lock-Free Compare-and-Swap Pattern

## Learning Objectives

By the end of the session you can:

- Explain why check-then-act fails under concurrency.
- Write a compare-and-set retry loop.
- Use `updateAndGet` or `getAndUpdate`.
- Say when a lock or transaction is still needed.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Check, then act | 7 min |
| 0:17 | Act 2: A lock | 7 min |
| 0:24 | Act 3: Compare-and-swap | 7 min |
| 0:31 | Act 4: The loop in one call | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one. Open `UnsafeStock.buyOne` and point to
the gap between reading and writing. Then open `CasStock.buyOne` and read the
`while` loop aloud: read, check, swap if unchanged, else retry.

## Exercises

1. Count the retries in act three with 2, 8 and 32 buyers. What happens?
2. Record buyers in a `ConcurrentLinkedQueue`. Can stock and buyers still disagree?
3. Replace the sold counter in FlashSale with a `LongAdder`.
