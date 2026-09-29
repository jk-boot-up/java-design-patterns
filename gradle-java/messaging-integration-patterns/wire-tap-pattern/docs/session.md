# Session Guide — Wire Tap Pattern

## Learning Objectives

By the end of the session you can:

- Explain why observing traffic should not mean editing services.
- Attach and detach a tap.
- Mask sensitive fields in copies.
- Keep a slow tap off the main path.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Logging typed in by hand | 7 min |
| 0:17 | Act 2: A wire tap | 7 min |
| 0:24 | Act 3: Attach and detach | 7 min |
| 0:31 | Act 4: A second tap | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: a missing message and a full card
number. Open `Channel.send`: taps first, then the destination. End on act
five and compare the two timings.

## Exercises

1. Make the audit tap write to a file, on its own thread.
2. Add a tap that only copies refunds over £20.
3. Mask the order ID too, and decide whether that makes the audit useless.
