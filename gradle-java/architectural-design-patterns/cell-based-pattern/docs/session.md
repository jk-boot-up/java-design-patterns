# Session Guide — Cell-Based Architecture Pattern

## Learning Objectives

By the end of the session you can:

- Explain blast radius.
- Route customers to cells with a placement table.
- Release to one cell first.
- Name the costs of running many cells.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One shared stack | 7 min |
| 0:17 | Act 2: Cells | 7 min |
| 0:24 | Act 3: A small blast radius | 7 min |
| 0:31 | Act 4: Add a cell | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 30 failures with act three's 10.
Open `CellRouter`: a placement map and one method that forwards. End on act
five and ask which reports in a real shop would need to ask every cell.

## Exercises

1. Deploy to cells one at a time, checking failures after each, and stop at the first failure.
2. Move customer C-5 from cell-2 to cell-4, including its orders.
3. Place customers by a hash of their ID instead of a table. What happens when you add a cell?
