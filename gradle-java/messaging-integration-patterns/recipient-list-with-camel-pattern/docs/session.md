# Session Guide — Recipient List with Apache Camel Pattern

## Learning Objectives

By the end of the session you can:

- Use `recipientList()` with a method that computes recipients.
- Add rule-based recipients without changing the route.
- Change the routing table while routes run.
- Explain what Camel does, and does not do, when a recipient fails.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Every order to every warehouse | 7 min |
| 0:17 | Act 2: A recipient list | 7 min |
| 0:24 | Act 3: Rules add recipients | 7 min |
| 0:31 | Act 4: The table changes while running | 7 min |
| 0:38 | Act 5: One recipient fails | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `ShopRoutes`: the recipient list is two lines.
Open `RoutingTable.recipients`: plain Java. End on act five's two lines.

## Exercises

1. Add `stopOnException()` and see which recipients still get ORD-1.
2. Add `parallelProcessing()` and explain why the order of arrival changes.
3. Send failed copies to a retry route instead of throwing.
