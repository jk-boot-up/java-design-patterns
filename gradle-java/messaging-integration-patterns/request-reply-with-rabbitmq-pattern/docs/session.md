# Session Guide — Request-Reply with RabbitMQ Pattern

## Learning Objectives

By the end of the session you can:

- Send requests with `replyTo` and `correlationId`.
- Match replies to requests by ID.
- Use direct reply-to or an exclusive queue as a return address.
- Use message expiry so an abandoned request is never handled late.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Replies taken in arrival order | 7 min |
| 0:17 | Act 2: Correlation IDs | 7 min |
| 0:24 | Act 3: Return addresses | 7 min |
| 0:31 | Act 4: Many in flight | 7 min |
| 0:38 | Act 5: A reply that never comes | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Compare act one's wrong pairs with act
two's right ones. Open `Requester.send`: two properties. End on act five's
expiry.

## Exercises

1. Remove the expiry in act five and show the mug being reserved late.
2. Replace the requester with Spring AMQP's `convertSendAndReceive`.
3. Run two inventory services and see replies still matched.
