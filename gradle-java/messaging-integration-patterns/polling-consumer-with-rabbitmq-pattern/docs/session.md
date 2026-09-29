# Session Guide — Polling Consumer with RabbitMQ Pattern

## Learning Objectives

By the end of the session you can:

- Poll a queue with `basicGet` and acknowledge each message.
- Explain what unlimited push does to a slow receiver.
- Use `basicQos` to push with a limit.
- Weigh polling intervals against empty requests.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Push with no limit | 7 min |
| 0:17 | Act 2: A polling consumer | 7 min |
| 0:24 | Act 3: Pausing is not polling | 7 min |
| 0:31 | Act 4: When nothing is happening | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Compare act one's 50 in hand with act
two's 5. Open `LabelPrinter`: `poll` and `subscribe`. End on act four's 600
empty polls and the prefetch of 5.

## Exercises

1. Try prefetch 1 and prefetch 50, and describe the difference.
2. Poll every second instead of every tenth, and count the empty polls.
3. Replace the polling loop with Spring AMQP's `receive()`.
