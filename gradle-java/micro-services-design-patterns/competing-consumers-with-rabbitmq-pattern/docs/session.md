# Session Guide — Competing Consumers with RabbitMQ Pattern

A 60-minute session built around one question: once the queue is a real broker that hands work out, how much may one worker hold, and when does the broker count the work as done?

## Learning Objectives

1. Say, in plain words, what a consumer, an acknowledgement, automatic acknowledgement, prefetch and the redelivered flag are.
2. Show that RabbitMQ's default prefetch, no limit, hands a whole queue to the first consumer.
3. Explain the trade between prefetch 1 and a higher prefetch, with the counts from act three.
4. Explain why a consumer that dies hands back every order it held, and why all of them are marked seen before.
5. Say what automatic acknowledgement costs, and why a poison order goes round for ever on a classic queue.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The kitchen analogy, and the plain-Java version recapped in two minutes |
| 0:08–0:15 | Act one: one picker, then three, and the spread described as a range |
| 0:15–0:27 | Acts two and three: no limit, then prefetch 10 and prefetch 1 |
| 0:27–0:40 | Act four: the crash mid-work |
| 0:40–0:47 | Act five: no saying done |
| 0:47–0:55 | Act six: the bill, and the verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd micro-services-design-patterns/competing-consumers-with-rabbitmq-pattern
./gradlew -q run
```

Act one: why does the 300-order line print words rather than three numbers? Act two: the fast picker was listening, so why was it handed 0? Act three: with prefetch 10, the queue was empty and the fast picker idle; where were the other 10 orders? Act four: why were ORD-4 and ORD-5 marked seen before when nobody had started them? Act five: the queue was empty before the crash; what does that tell you about when the broker forgot the orders? Act six: what would stop ORD-13?

Then open `src/main/java/com/jk/explore/competingconsumersrabbitmq/Picker.java` and read `start` aloud. The prefetch is one call, `basicQos`, and the acknowledgement mode is one argument to `basicConsume`.

## Discussion

Ask the room what prefetch they would pick for a picker whose work takes half a second and a network trip that takes one millisecond. Then for work that takes one millisecond. The answer changes, and nobody picks "no limit".

Then ask what a picker should do with an order marked seen before. Skip it? That loses ORD-4 and ORD-5 in act four, which were never started. Check the stock ledger first? That is the only answer that works, and it is the receiver's job, not the broker's.

## Exercises

1. Give the slow picker in act two a prefetch of 1 and predict both counts before you run it.
2. Change act four's prefetch from 5 to 1, and predict how many orders come back and how many are marked seen before.
3. Make the picker skip any order marked seen before, run act four, and count what is lost.
4. Make the picker check the stock ledger before reserving, so ORD-3 is reserved once.
5. Declare the poison queue as a quorum queue with a delivery limit, and find out what happens to ORD-13.

Close with the verdict: set a prefetch, say done after the work, and put a limit on how often one order may be handed out.
