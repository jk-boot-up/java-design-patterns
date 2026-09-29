# Session Guide — Table-Driven State Machine Pattern

## Learning Objectives

By the end of the session you can:

- Say what a state machine is, using an order.
- Write the allowed moves as a table.
- Refuse any move not in the table, with a clear message.
- Add a rule by adding a row.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Rules in if statements | 7 min |
| 0:17 | Act 2: The table | 7 min |
| 0:24 | Act 3: Wrong moves refused | 7 min |
| 0:31 | Act 4: A new rule | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: two bugs that nobody would spot in a
review. Then open `TransitionTable.orders()`: five lines that are the whole
rule book. Ask learners to draw it as boxes and arrows on paper before showing
the diagram.

## Exercises

1. Allow cancelling a PAID order, which should refund it. Is that one row, or a row and some code?
2. Add a `LOST` status for parcels that never arrive. Which actions lead in and out?
3. Attach an action to a move: print "email sent" whenever an order becomes SHIPPED.
4. Write a test that no status can reach PLACED again.
