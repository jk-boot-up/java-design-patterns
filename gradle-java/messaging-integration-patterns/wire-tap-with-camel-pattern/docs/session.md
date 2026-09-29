# Session Guide — Wire Tap with Apache Camel Pattern

## Learning Objectives

By the end of the session you can:

- Add a `wireTap()` to a Camel route.
- Explain why the tap shares the message object, and fix it with `onPrepare()`.
- Show that a failing tap does not affect the main route.
- Explain the lag of an asynchronous tap.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A tap on the route | 7 min |
| 0:17 | Act 2: Not a copy after all | 7 min |
| 0:24 | Act 3: onPrepare: a real copy | 7 min |
| 0:31 | Act 4: The audit stops | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Compare act two's masked ORD-1 with act three's full card
number. Open `ShopRoutes`: the only difference is the `onPrepare` line. End
on act five's lag.

## Exercises

1. Make `PaymentMessage` immutable and remove `onPrepare`; explain why the trap disappears.
2. Tap to a SEDA queue with a size limit, and see what happens when it fills.
3. Add a second tap for a sales dashboard that sums net takings.
