# Guaranteed Delivery Pattern — Video Narration Script

## 1. Guaranteed Delivery

Hello, and welcome. This video explains the Guaranteed Delivery pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. With guaranteed delivery, every message is stored safely on disk before it is accepted. It is marked as done only after it has been delivered. And after a crash, everything not marked as done is delivered again. Think of recorded delivery at the post office. Each parcel is written in a ledger before you get your receipt. The recipient signs when it arrives. If a van breaks down, the ledger says exactly what to send out again. In this video, the domain is an online shop. It sends an order confirmation email for every order, through a queue in front of a slow email provider. By the end, you will hear how messages in memory are lost. How a journal on disk keeps them. How acknowledgements work. And why guaranteed means at least once.

## 2. The Scenario

Here is the scenario. Every order gets a confirmation email. The emails wait in a queue, because the email provider is slow. And that queue lived only in the server's memory.

## 3. Act One — Only in memory

First demo: confirmation emails queued in memory. The email provider is slow today. Ten emails are waiting in the queue. The server restarts, for an ordinary update. The queue lived in memory. Now it is empty. Ten customers will never hear that their order was received.

## 4. Act Two — Written to disk first

Second demo: every message is written to disk before it is accepted. Each email is written to a journal file. Only when it is safely on the disk is the email accepted. Ten emails, ten lines in the file. The server restarts. It reads the file. Ten emails are still waiting.

## 5. Act Three — Acknowledgements

Third demo: delivered messages are acknowledged. When an email is sent, the journal writes a second line: acknowledged. Six emails are sent and acknowledged. Then the server crashes. After the restart, only emails seven to ten are still waiting. They are sent. All ten customers get exactly one email.

## 6. Act Four — At least once

Fourth demo: a crash between sending and acknowledging. Email eleven is sent. And the server crashes, before it writes the acknowledgement. After the restart, the journal cannot know it was sent. So it sends it again. The customer gets two emails. Guaranteed delivery means at least once. Not exactly once.

## 7. Act Five — The bill

Fifth demo: the bill. The disk is now in the path of every message. Ten emails cost ten forced disk writes to accept, and ten more to acknowledge. The journal keeps growing, until someone trims the acknowledged lines. And the receivers must cope with the odd duplicate.

## 8. The Pattern

Let's name the pattern. Write each message to disk, and make sure it has reached the disk. Only then tell the sender: accepted. When it is delivered, write a second line: acknowledged. After a crash, read the file, and deliver every message that was never acknowledged.

## 9. Who Does What

Here is who does what. The journal writes messages and acknowledgements to one file, and finds what is still waiting. The email sender stands in for the slow email provider. And the memory queue is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. RabbitMQ has durable queues and persistent messages. So does J M S. Kafka writes every message to a log, copied across machines. And the transactional outbox stores messages in the database first, for the same reason.

## 11. When To Use It

So, when should you use it? For messages that must not be lost. Orders, payments, and confirmations. Expect duplicates, and make receivers cope with them. Trim what has been acknowledged. And for messages that are cheap to lose, such as live price updates, skip it.

## 12. Thanks for Watching

That's the Guaranteed Delivery pattern. If you remember one sentence, make it this one. Write it down before you say yes, and cross it off only when it has arrived. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make the email sender skip any email it has already sent. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
