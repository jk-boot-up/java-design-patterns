# Session Guide — Space-Based Architecture Pattern

## Learning Objectives

By the end of the session you can:

- Explain why a central database limits scaling.
- Describe processing units, the data grid and the data writer.
- Explain eventual consistency with the last-kettle example.
- Decide when the trade-off is acceptable.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One database for everyone | 7 min |
| 0:17 | Act 2: Processing units | 7 min |
| 0:24 | Act 3: The data grid | 7 min |
| 0:31 | Act 4: The database catches up | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's two timings. Open `ProcessingUnit`:
memory only. Then `DataGrid.flush` and `DataWriter`. End on act five: which
things in a shop could accept that risk, and which never could?

## Exercises

1. Flush the grid after every 10 orders. How often does the last kettle sell twice now?
2. Reserve a small safety stock on each unit so it stops selling before the true zero.
3. Add a unit while the sale is running. How does it get its copy of the stock?
