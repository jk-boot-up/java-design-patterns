# Session Guide — Guaranteed Delivery with RabbitMQ Pattern

## Learning Objectives

By the end of the session you can:

- Tell a durable queue from a persistent message.
- Use publisher confirms so the sender knows a message is stored.
- Acknowledge only after the work is done.
- Explain why guaranteed means at least once.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Durable queue, transient messages | 7 min |
| 0:17 | Act 2: Persistent and confirmed | 7 min |
| 0:24 | Act 3: Acknowledged after sending | 7 min |
| 0:31 | Act 4: A crash before the acknowledgement | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Compare act one's 0 with act two's
10. Open `Outbox`: the difference is one property and one confirm. End on act
four's two emails.

## Exercises

1. Make the sender skip a message whose redelivered flag is set and whose id it has already sent.
2. Declare the queue as a quorum queue and repeat act two.
3. Measure how much slower 1,000 confirmed sends are than unconfirmed ones.
