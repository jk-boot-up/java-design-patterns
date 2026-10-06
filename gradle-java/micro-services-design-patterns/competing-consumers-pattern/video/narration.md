# Competing Consumers Pattern — Video Narration Script

## 1. Competing Consumers

Hello, and welcome. This video explains the Competing Consumers pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Competing consumers means several workers take messages from the same queue. Each message goes to exactly one of them. So the work is shared, without the workers ever talking to each other. Think of a supermarket with one long queue and several tills. Whichever till is free calls the next customer. Each customer is served once, and the tills never need to agree on anything. In our online store, the work waiting to be done is a queue of orders. By the end, you will hear one worker, then three, share the same queue. Every message handled exactly once. The order of messages given up. A failed message taken over. And the costs: duplicates, and workers stuck waiting for something they share.

## 2. The Scenario

Here is the scenario. Orders wait in a queue to be processed. One worker cannot keep up. We want to add a second worker, and a third. Without rewriting anything. And without handling any order twice. So here is the question. How?

## 3. One Consumer, Then Three

First demo: one consumer, then three. A consumer is simply a worker that takes messages from the queue. There are six slow jobs. With one consumer, one job is in progress, and five are waiting. With three consumers, three are in progress, and three are waiting. The consumers do not talk to each other. They just take from the same queue.

## 4. The Pattern

Now, the pattern. Several consumers read from one queue. Each message goes to exactly one of them. If a message is not finished, it goes back on the queue. And to add capacity, you simply add another consumer. Nothing else changes.

## 5. Each Message Is Handled Once

Second demo: each message is handled once. A thousand orders, and four consumers. The orders were handled a thousand times in total. And they were a thousand different orders. None twice, and none missed. Which consumer got which order is not decided in advance. And it does not matter.

## 6. The Order Is Not Kept

Third demo: the order is not kept. Orders one, two, and three are put on the queue, in that order. But the consumer handling order one is slow. So they finish as two, then three, then one. If order two depends on order one, that is a bug. Competing consumers give up ordering, to gain capacity.

## 7. A Consumer Fails, Another Takes Over

Fourth demo: a consumer fails, and another takes over. The first attempt fails. The message goes back to the queue. And a second attempt succeeds. The message was not lost. Because it was never truly removed from the queue until it was finished.

## 8. At Least Once, So A Duplicate

Fifth demo: a duplicate. A consumer charges a customer's card. Then it crashes, before it can say it has finished. So the message comes back, and the card is charged again. Two charges. Now try a consumer that remembers what it has already done. It charges only once. The queue promises to deliver each message at least once, not exactly once. So the consumer itself has to make a repeat harmless.

## 9. The Bill: The Same Downstream

Finally, the bill. Six consumers share a database that only lets two in at a time. Two consumers are inside. Four are waiting for a place. So four of the six are doing nothing useful. Adding consumers only helps while the thing they share still has room.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for several copies of a service, reading from the same queue. Look for Kafka consumer groups, several programs polling one Amazon queue, or RabbitMQ work queues. Look for a call that acknowledges or deletes a message after the work is done. Or a pool of threads, all taking tasks from one shared queue.

## 11. The Verdict

So, here is the verdict. Use competing consumers to scale work that can be done in any order. Where each item is independent of the others. Only confirm a message once the work is finished. Make every consumer safe to run twice on the same message. And size the number of consumers for the slowest thing they share. Do not use it where order matters. Unless the queue is split so that related messages always go to the same consumer.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? When one consumer can keep up, extra consumers only add cost and risk. And when order matters, competing consumers are the wrong choice, until the queue is split by the thing that needs ordering.

## 14. Thanks for Watching

That's the Competing Consumers pattern. If you remember one sentence, make it this one. Competing consumers share the work by giving up ordering, and the consumer itself must handle the duplicates the queue cannot avoid. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make the consumer safe to run twice. Then prove it, by delivering every message twice. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
