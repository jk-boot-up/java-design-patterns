# Session Guide — Message Channel with RabbitMQ Pattern

A 60-minute session built around one question: once the channel is a real broker in its own process, what does it keep, for how long, and who has to ask?

## Learning Objectives

1. Say, in plain words, what a broker, a queue, an exchange, an acknowledgement and a publisher confirm are.
2. Show a message waiting in a queue for a receiver that does not exist yet.
3. Explain why a receiver that crashes before saying done costs a second delivery rather than a lost order.
4. Show that a durable queue is not enough, and name the second setting a restart depends on.
5. Say what a full RabbitMQ queue does by default, and what it takes to make it refuse out loud.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The post office analogy, and the partner project recapped in two minutes |
| 0:08–0:18 | Acts one to three: the direct call, the channel, and nobody listening |
| 0:18–0:30 | Act four: saying done, and the order seen twice |
| 0:30–0:42 | Act five: the restart |
| 0:42–0:50 | Act six: the bill |
| 0:50–0:55 | The verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd messaging-integration-patterns/message-channel-with-rabbitmq-pattern
./gradlew -q run
```

Act one: how many checkouts failed, and did selling actually need the warehouse? Act two: did checkout wait for the warehouse? Act three: how many orders did the broker hold with no receiver anywhere, and in what order did they come out? Act four: how many deliveries, how many orders picked, and what told the second picker it might be a repeat? Act five: both queues were durable, so why did one come back empty? Act six: what would have happened to the three refused orders without receipts?

Then open `src/main/java/com/jk/explore/messagechannelrabbitmq/Channel.java` and read `send` and `sendWithoutWritingDown` aloud. The only difference between the two is one argument to `basicPublish`.

## Discussion

Ask the room which orders in a real store may be held in memory only. Stock-level refreshes that the next one replaces, perhaps. A pick order for a paid basket, never. The broker cannot tell the difference; the sender has to.

Then ask what the warehouse should do with an order marked as seen before. Pick it again? Look it up first? There is no answer in the broker, which is the point: at-least-once delivery hands the duplicate problem to the receiver.

## Exercises

1. Change the fifth act so both channels send with `sendWithoutWritingDown`, and predict both counts before you run it.
2. Remove `x-overflow` from `openWithRoomFor`, run the sixth act, and find out which five orders are left waiting.
3. Turn automatic acknowledgement on in `receiveEachInto`, make the warehouse throw on the second order, and count what is lost.
4. Make the warehouse remember the order numbers it has picked, and skip an order marked as seen before that it has already picked.
5. Declare the fifth act's queues as not durable, restart the broker, and say what happens to the queues themselves.

Close with the verdict: write down the queue and the message, say done after the work and not before, and give every queue a limit and a receipt.
