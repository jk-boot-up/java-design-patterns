# Session Guide — Event-Carried State Transfer Pattern

## Learning Objectives

By the end of the session you can:

- Contrast thin notification events with state-carrying events.
- Keep a local copy filled from events.
- Explain eventual consistency with a concrete stale read.
- Guard a copy against out-of-order events with versions.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A thin event, and a call back | 7 min |
| 0:17 | Act 2: The event carries the address | 7 min |
| 0:24 | Act 3: The copy lags behind | 7 min |
| 0:31 | Act 4: Events out of order | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 0 of 100 with act two's 100 of 100.
Open `ReplicaShipping.on`: one map, one version check. End on act four's two
lines.

## Exercises

1. Add a `CustomerDeleted` event and remove the copy when it arrives.
2. Let shipping keep only the city and postcode it needs, not the whole address.
3. Replay all events to rebuild shipping's copy from scratch.
