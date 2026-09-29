# Session Guide — Scheduler Pattern

## Learning Objectives

By the end of the session you can:

- Explain why a lock alone cannot choose who goes next.
- Build a scheduler around a lock, a condition and a policy.
- Swap policies.
- Prevent starvation with ageing.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A fair lock | 7 min |
| 0:17 | Act 2: Express first | 7 min |
| 0:24 | Act 3: A replaceable policy | 7 min |
| 0:31 | Act 4: Nobody waits for ever | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one's print order aloud. Open
`Scheduler.enter`: add to the list, wait until free and chosen, remove. Then
show that the two policies are one-line comparators. End on act four's two
orders side by side.

## Exercises

1. Add a policy: oldest first, but express jobs count as 30 seconds older.
2. Give each job a deadline and print the one closest to its deadline first.
3. Replace the scheduler with a `PriorityBlockingQueue` and one printing thread. What changes for the stations?
