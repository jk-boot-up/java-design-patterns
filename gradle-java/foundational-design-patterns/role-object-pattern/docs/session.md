# Session Guide — Role Object Pattern

## Learning Objectives

By the end of the session you can:

- Explain why subclasses fail when an object's kind changes over time.
- Model an identity as a core object and each activity as a role.
- Add and remove roles at run time.
- Name the costs: asking first, and spread-out data.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A subclass per kind | 7 min |
| 0:17 | Act 2: One account, many roles | 7 min |
| 0:24 | Act 3: Roles with behaviour | 7 min |
| 0:31 | Act 4: Dropping a role | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: zero orders on the new object. Then open
`Account` (identity plus a map of roles) and `Roles` (three small classes).
Show that removing `Seller` leaves `Buyer` untouched.

## Exercises

1. Add an `Admin` role that can refund orders. Who is allowed to add it?
2. Keep the shop name when selling is suspended, so it can be restored later.
3. Print every account that currently plays the Seller role.
4. Stop the same role being added twice.
