# Session Guide — Priority Queue Pattern

## Learning Objectives

By the end of the session you can:

- Explain when a FIFO queue fails a deadline.
- Order a queue by priority, then age.
- Prevent starvation with a reserved share.
- Decide who is allowed to set priorities.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: First come, first served | 7 min |
| 0:17 | Act 2: A priority queue | 7 min |
| 0:24 | Act 3: A flood of standard orders | 7 min |
| 0:31 | Act 4: Starvation, and a reserved share | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 9:10 with act two's 9:01. Open
`Picking.priority`: one comparator. End on act four's two numbers: 0 of 20 and
20 of 20.

## Exercises

1. Add a third priority, express, above same-day.
2. Promote standard orders older than 15 minutes instead of reserving picks.
3. Only allow same-day on orders placed before 11:00.
