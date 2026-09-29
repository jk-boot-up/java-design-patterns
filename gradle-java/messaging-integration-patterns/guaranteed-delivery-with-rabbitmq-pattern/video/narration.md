# Guaranteed Delivery with RabbitMQ Pattern — Video Narration Script

## 1. Guaranteed Delivery with RabbitMQ

Hello, and welcome. This video explains the Guaranteed Delivery pattern, with a real RabbitMQ broker, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Guaranteed delivery means a message, once accepted, is never lost. Not when the program crashes. Not when the broker restarts. RabbitMQ is an open-source message broker, a separate program that holds messages, and it can give that guarantee if you ask for it correctly. Think of recorded delivery at the post office. You get a receipt when you hand the letter over. And it is signed for at the other end. In this video, the domain is an online shop's order confirmation emails. By the end, you will hear which RabbitMQ settings make the guarantee. What happens when one is missing. And why a guaranteed message can still arrive twice.

## 2. The Scenario

Here is the scenario. The shop's confirmation emails wait on a queue, while the email provider is slow. The broker restarted, for an update. Ten emails vanished. Ten customers never heard that their order was received.

## 3. Act One — Durable queue, transient messages

First demo: a durable queue, but messages that are not persistent. The queue itself is written to disk. The messages are not. Ten emails are waiting. The broker restarts. The queue is still there. It is empty. A durable queue is not enough. Each message must be marked persistent too.

## 4. Act Two — Persistent and confirmed

Second demo: persistent messages, and publisher confirms. Each email is now marked persistent. And the sender waits for the broker to confirm it is stored. The broker restarts. All ten emails are still waiting.

## 5. Act Three — Acknowledged after sending

Third demo: acknowledged after sending. The email sender tells the broker each email is done, only after sending it. It sends six, and stops. Four are still waiting. A new sender takes the rest. Ten of ten, each sent once.

## 6. Act Four — A crash before the acknowledgement

Fourth demo: a crash before the acknowledgement. The sender sends email eleven. Then it dies, before saying it is done. The broker puts the email back on the queue. The next sender gets it again. Marked as redelivered. The customer receives it twice. Guaranteed delivery means at least once. The redelivered mark lets a receiver check first.

## 7. Act Five — The bill

Fifth demo: the bill. Every email now waits for a disk write, and a confirm, before checkout moves on. And the broker is one more system to run, back up, and watch. One broker is still one disk. Production copies queues across several brokers.

## 8. The Pattern, in RabbitMQ

Let's name the pattern, in RabbitMQ's words. A durable queue, which survives a restart. Persistent messages, written to disk. Publisher confirms, so the sender knows each message is stored. And acknowledgements, sent only after the work is done.

## 9. Who Does What

Here is who does what. The broker class starts RabbitMQ in a container, and can restart it. The outbox sends each email, and waits for the confirm. The email sender sends each email, and then acknowledges it. And poll waits for real conditions, never a fixed time.

## 10. Where You Have Seen It

You have probably met this already. RabbitMQ's confirms and acknowledgements. Kafka, which waits for every copy of a message to be stored. And Amazon SQS, where a message stays until the receiver deletes it.

## 11. When To Use It

So, when should you use it? For messages someone would miss. Orders, payments, confirmations. Use all four settings. Expect duplicates, and make receivers cope. And copy queues across brokers in production.

## 12. Thanks for Watching

That's Guaranteed Delivery, with RabbitMQ. If you remember one sentence, make it this one. Store it, confirm it, and acknowledge it only when the work is done. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It needs Docker running, and starts the broker for you. Here is one exercise to try. Make the sender skip a redelivered email it has already sent. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
