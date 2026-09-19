# Competing Consumers Pattern — Video Narration Script

## 1. Competing Consumers

Hello, and welcome. This video explains the Competing Consumers pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: competing consumers means several workers take messages from the same queue. Each message goes to exactly one of them, and the work is shared without the workers ever having to coordinate. This is another project in the microservices category, whose subject is how many small services stay reliable when they talk to each other. In our online store, the work waiting to be done is a queue of orders. By the end you will see one worker and three workers take from the same queue, see every message handled exactly once, see ordering given up, see a failed message taken over, and see the bills: duplicates, and workers that can only wait for a shared limit.

## 2. The Scenario

Here is the scenario. Orders wait in a queue to be processed. One worker cannot keep up. We want to add a second, and a third, without rewriting anything, and without handling an order twice. The question: how?

## 3. One Consumer, Then Three

First, one consumer, then three. Six slow jobs. With one consumer, one is in progress and five are waiting. With three consumers, three are in progress and three are waiting. The consumers do not talk to each other. They just take from the same queue.

## 4. The Pattern

The pattern. Several consumers read from one queue. Each message goes to exactly one of them. A message that is not finished goes back on the queue. And you add capacity by adding a consumer, without changing anything else.

## 5. Each Message Is Handled Once

Second, each message is handled once. A thousand orders, four consumers. The orders were handled a thousand times in all, and they were a thousand different orders. None twice, and none missed. Which consumer got which order is not defined, and does not matter.

## 6. The Order Is Not Kept

Third, the order is not kept. Orders one, two and three are published in that order. Order one's consumer is slow. They finish as two, three, one. If order two depends on order one, that is a bug. Competing consumers give up ordering to gain capacity.

## 7. A Consumer Fails, Another Takes Over

Fourth, a consumer fails, and another takes over. The first attempt fails. The message is given back to the queue, and a second attempt succeeds. The message was not lost, because it was never really removed until it was finished.

## 8. At Least Once, So A Duplicate

Fifth, at least once, so a duplicate. A consumer charges the card, and crashes before it can say it finished. The message comes back, and the card is charged again: two charges. A consumer that remembers what it has done charges once. The queue cannot give you exactly once. The consumer has to.

## 9. The Bill: The Same Downstream

Last, the bill. Six consumers share a database that lets only two in at a time. Two are inside. Four are waiting for a place. Four of the six are doing nothing useful. Adding consumers only helps while the thing they share has room.

## 10. How To Recognise It

How do you recognise this in code you did not write? Several instances of a service reading the same queue or topic partition group. Kafka consumer groups, SQS with several pollers, RabbitMQ work queues. An acknowledge or delete call after the work is done. A thread pool whose tasks come from one shared queue.

## 11. The Verdict

Here is my verdict, plainly. Use competing consumers to scale work that can be done in any order, where each item is independent. Acknowledge only when finished, make every consumer safe to run twice on the same message, and size the pool for the slowest thing they share. Do not use it where order matters, unless the queue is partitioned by the key that carries the order.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? When one consumer keeps up, extra consumers are cost and risk. When order matters, competing consumers are wrong until the queue is partitioned.

## 14. Thanks for Watching

That's Competing Consumers. If you take one sentence away, take this one: competing consumers share the work by giving up ordering, and the duplicate they cannot avoid must be handled by the consumer. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, make the consumer safe to run twice, and prove it by delivering every message twice. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
