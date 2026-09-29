# Session Guide — Request-Reply with Correlation Identifier Pattern

## Learning Objectives

By the end of the session you can:

- Explain why replies arrive out of order.
- Correlate replies with a unique request ID.
- Use a return address to share a service between requesters.
- Handle replies that never arrive.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Replies matched by order | 7 min |
| 0:17 | Act 2: Correlation IDs | 7 min |
| 0:24 | Act 3: Return addresses | 7 min |
| 0:31 | Act 4: Many in flight | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one's swapped answers. Open `Requester`: the
waiting table, `send`, and the listener that looks up each reply's
correlation ID. End on act five and ask how checkout could find out whether the
lost reservation happened.

## Exercises

1. Remove timed-out requests from the waiting table automatically.
2. Add a 'status of request' query so checkout can ask about WEB-24.
3. Make the inventory service reply twice by mistake. What should the requester do with the second reply?
