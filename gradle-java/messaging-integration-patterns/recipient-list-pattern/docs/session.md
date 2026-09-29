# Session Guide — Recipient List Pattern

## Learning Objectives

By the end of the session you can:

- Tell a recipient list from a router and from a broadcast.
- Compute recipients from a message and rules.
- Change routing without changing senders.
- Handle partly failed sends.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Everything everywhere | 7 min |
| 0:17 | Act 2: A recipient list | 7 min |
| 0:24 | Act 3: Rules add recipients | 7 min |
| 0:31 | Act 4: A changed table | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 20 deliveries with act two's 8. Open
`RecipientList.recipientsFor`: categories through the table, then rules. End
on act five: what should happen to the half of ORD-1 that was sent?

## Exercises

1. Retry failed recipients once, then send the order to a problem list.
2. Add a rule: orders to Scotland also go to the north warehouse.
3. Print which recipients each rule added, for an audit log.
