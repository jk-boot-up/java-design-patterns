# Session Guide — Write-Behind Cache Pattern

## Learning Objectives

By the end of the session you can:

- Explain write-through and write-behind in one sentence each.
- Show why write-behind turns many writes into few.
- Name the crash window and what is lost in it.
- Decide which data may be written behind, and which never.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Write every change | 7 min |
| 0:17 | Act 2: Write behind | 7 min |
| 0:24 | Act 3: The database goes down | 7 min |
| 0:31 | Act 4: A crash before the flush | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare acts one and two: thirty writes against three.
Then open `WriteBehindStore.java` and follow a change through `set`, the dirty
set, and `flush`. Spend the most time on act four: every learner should be able
to say exactly what was lost and why.

## Exercises

1. Flush automatically when 100 carts are dirty, as well as every five seconds.
2. Add a `shutdown()` that flushes before the process stops. Which crashes does it not help with?
3. Count how many changes were lost across a day if the server crashes once, with flushes every 1 s and every 60 s.
4. Make order placement write straight through, while cart changes stay behind.
