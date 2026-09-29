# Session Guide — Materialized View Pattern

## Learning Objectives

By the end of the session you can:

- Explain why asking several services on every read is slow and fragile.
- Build a view that updates itself from events.
- Explain eventual consistency with the shipped order that still reads placed.
- Rebuild a view from the event log.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Asking three services | 7 min |
| 0:17 | Act 2: A ready-made view | 7 min |
| 0:24 | Act 3: A moment behind | 7 min |
| 0:31 | Act 4: Rebuild from the events | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and start with act one: seven calls and a failed page.
Then open `OrderHistoryView.java` and read its one method, `on`, one event at a
time: placed adds a row, shipped changes a status, renamed rewrites names. Act
three is the one to pause on, because the lag is the price every learner must
be able to explain.

## Exercises

1. Add a `total spent` figure per customer to the view. Which events must change it?
2. Add an `OrderCancelled` event. Update the view, and rebuild it from the log.
3. Count how many rows a rename rewrites for a customer with 100 kettle orders. Is that a problem?
4. Deliver the events in a different order. Which orders break the view, and how would you guard against it?
