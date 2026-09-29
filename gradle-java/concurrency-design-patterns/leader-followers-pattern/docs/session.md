# Session Guide — Leader/Followers Pattern

## Learning Objectives

By the end of the session you can:

- Describe the leader, followers and promotion.
- Implement leadership with a lock.
- Compare with a dispatcher and hand-off queue.
- Explain the ordering cost.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A dispatcher that hands off | 7 min |
| 0:17 | Act 2: Leader and followers | 7 min |
| 0:24 | Act 3: Receive, promote, handle | 7 min |
| 0:31 | Act 4: Every thread works | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act one's 20 hand-offs with act three's 0.
Open `LeaderFollowers.takeTurns`: lock, take, unlock, handle. That order of
four lines is the whole pattern. End on act five with the place and cancel
messages.

## Exercises

1. Route messages for the same order to the same thread, and show place finishes before cancel.
2. Count how many orders each pool thread handled. Is it even?
3. Replace the lock with a Semaphore of one permit.
