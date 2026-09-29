# Session Guide — Routing Slip Pattern

## Learning Objectives

By the end of the session you can:

- Explain how a routing slip differs from a fixed pipeline.
- Write slips from a message's properties.
- Keep steps unaware of what follows them.
- Say when a process manager is needed instead.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One fixed pipeline | 7 min |
| 0:17 | Act 2: Routing slips | 7 min |
| 0:24 | Act 3: Steps pass it on | 7 min |
| 0:31 | Act 4: A new step | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 24 visits with act three's 15.
Open `RoutingSlip.slipFor`: the only place routes are decided. Then `route`:
pop the next step, run it, repeat. End on act five.

## Exercises

1. Add a 'loyalty-points' step for registered customers.
2. Put the slip into the message as text and have a separate service read it.
3. Rewrite act five with a process manager that asks for ID and then continues.
