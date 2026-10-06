# Transactional Outbox with Debezium Pattern — Video Narration Script

## 1. Transactional Outbox with Debezium

Hello, and welcome. This video explains the Transactional Outbox pattern in Java, using a real Postgres database, a real Kafka broker, and a tool called Debezium in between. This video is presented by Jayasekhar Konduru. First, a simple definition. When you must save something, and also tell others about it, do not do two separate things that can half happen. Save the message in your own database, beside the record, in one single save. And let something else send it out later. Think of an office out-tray. You file your copy and drop the letter in the tray, in one action. The post room sends it later. In our online store, when a customer checks out, the orders service saves the order, and an order placed message, together. And Debezium sends that message on. By the end, you will hear a message sent for a row that was already deleted. A database keeping its history for a reader that was switched off. And the same message sent twice.

## 2. The Scenario

Here is the scenario. When a customer checks out, the orders service saves the order in its own database. That database is Postgres. The rest of the shop, notifications, stock, and shipping, hears about new orders through a message broker. That broker is Kafka. The shop wants three things. Every saved order is announced. Nothing is announced that was not saved. And each order's events, placed, paid, and shipped, are heard in the order they happened.

## 3. Two Writes, One Crash

First demo: two writes, and one crash. There is no outbox yet. Checkout saves the order in Postgres, and then sends the message to Kafka itself. The program dies between the two. Order one is in Postgres. Kafka has no message. The customer is charged, and nobody is told. So swap the two lines. Send first, then save, and die in between. Now Kafka has one message, and order two is not in Postgres. The shop has announced an order that does not exist. Two systems, two steps, and no transaction that covers both.

## 4. Postgres's Words

Before the fix, some words, in plain language. Picture an office where every piece of paper is first copied into a journal, automatically. Postgres has exactly that. Before it changes any table, it writes the change into a journal on disk. So it can recover after a crash. Postgres calls it the write-ahead log. Normally, only Postgres reads it. But with one setting switched on, an outside program can read the changes too. That outside reader gets a bookmark in the journal. Postgres calls that bookmark a replication slot. And Postgres keeps every page of the journal that the reader has not yet confirmed.

## 5. Debezium's Words

Debezium is that outside reader. It holds the bookmark, receives every saved change, and turns each one into a message. This is called change data capture. One part of Debezium takes each new row in the outbox table, and turns it into one clean message. The order I D becomes the message's key. And the row's own I D travels with the message, as a label. Debezium also writes down how far through the journal it has read. Usually, Debezium runs as a program of its own. Here, it runs inside the demo's own Java program. That saves a third container, and it reads the journal in exactly the same way.

## 6. One Transaction, And Debezium Sends

Second demo: one transaction, and Debezium sends. Postgres is started with its journal readable from outside. Debezium, version three point six, runs inside the program, and holds its bookmark. Checkout now writes each order, and a row in the outbox table, in one transaction. And it saves them together. Checkout has no Kafka code at all. Three orders, and three outbox rows. Debezium reads the three saves from the journal, and sends three messages. Then order four writes both rows. But the card is declined, and the whole transaction is undone. Order five saves after it. Kafka now holds four messages, and not one for order four. The journal only passes on work that was actually saved. So an order and its message live or die together.

## 7. The Log, Not The Table

Third demo, and this is the headline of the video. This time, each transaction writes the outbox row. And then deletes it again, before saving. Three orders. The outbox table ends up with no rows at all. And Kafka still receives three messages. Debezium never looked at the table. It read the inserts from the journal, where they were written before the delete. A relay that reads the table, like the one in the plain Java version, would have found nothing to send. Debezium recommends working this way. Because then the outbox table never needs cleaning.

## 8. Where Each Piece Lives

Here is where each piece lives, in words. Checkout writes to Postgres, and to nothing else. Postgres writes every change into its journal first. And it keeps the journal for the bookmark. Debezium receives the saved outbox changes. And it forwards each one to Kafka, keyed by the order. Only after Kafka accepts a message does Debezium write down how far it has read. That order of steps matters, and the fifth demo shows why.

## 9. Debezium Is Down

Fourth demo: Debezium is down. Debezium is stopped, so the bookmark has no reader. Checkout does not notice. It takes three orders, and Kafka receives nothing. Meanwhile, Postgres keeps every page of the journal that Debezium has not confirmed. And the amount it keeps keeps growing. By default, there is no limit at all. Debezium starts again, carries on from its bookmark, and sends all three orders. Nothing was lost. And nobody wrote any retry code. But remember that missing limit. If Debezium is switched off and forgotten, Postgres keeps its journal until the disk is full.

## 10. The Pattern In One Transaction

On the checkout's side, the whole pattern is one transaction. Switch off automatic saving. Insert the order: order one, customer one, a total of twenty-nine pounds ninety-five, status placed. Insert the outbox row. Its type is order placed, and it carries the order. Then save once, for both rows. What matters most is what is missing. Checkout never connects to Kafka. Debezium reads the saved rows from the journal.

## 11. Sent, But Not Written Down

Fifth demo: sent, but not written down. Debezium sends orders one and two to Kafka. Then it dies, before writing down how far it has read. Kafka holds two messages. Debezium starts again, from the last place it wrote down. The bookmark still holds those two changes, because they were never confirmed. So Debezium sends both again. Four messages, for two orders. Each pair carries the same message I D. Delivery is at least once. That is the price of writing down after sending. Writing down first would risk losing a message forever. And the unchanging I D is what lets a reader throw away the second copy.

## 12. Order Per Key, And The Bill

Sixth demo: ordering, and the bill. Three orders are placed, then paid, then shipped. Each step is its own transaction, and the orders take turns. Nine saves in all. Kafka splits the topic into three lanes, read side by side. It calls them partitions. The order I D picks the lane. And order is kept within a lane, never across lanes. Order one lands alone in one lane: placed, paid, shipped. Orders two and three share another lane, taking turns. And each keeps its own order. Then the bill. Two containers. Postgres started with its journal readable from outside. And one bookmark, with no limit on how much it keeps. So when Debezium is retired, the bookmark must be deleted too. The demo deletes it.

## 13. What The Simulation Left Out

How does this compare with the plain Java version? It got the whole pattern right. Both ways the two separate writes can fail. The message saved beside the order, in one transaction. Checkout carrying on while the sender is away. And the duplicate when the sender dies at the wrong moment. All of that holds here. What it left out is what a real database journal adds. Debezium reads the journal, not the table. So a deleted row is still sent. The bookmark keeps the journal for its reader, with no limit. An undone transaction never appears at all. And order is kept per key, and only per key.

## 14. The Verdict

So, here is the verdict. Save to one system only: the order, and its outbox row, in one transaction. Let change data capture carry the message out, from the database's own journal. Key each message by its order, so one order's messages stay in order. Watch the bookmark, and raise an alert when it stops moving. Delete it when Debezium is retired. And make every reader forgive a duplicate, by remembering the message I Ds it has already handled.

## 15. What Is Real Here

A quick, honest note about this demo. The database is Postgres, version eighteen point six. The broker is Kafka, version four point three point one. Each runs in a container that the demo starts and stops by itself. Debezium is version three point six point three, running inside the demo. You just need Docker switched on first. Every number you heard comes from the program's own output. So, when is this too much? If you cannot make your database's journal readable from outside, use a relay that checks the outbox table on a timer instead. It gives the same guarantee, at the price of a table to clean.

## 16. Thanks for Watching

That's Transactional Outbox, with Debezium. If you remember one sentence, make it this one. Save to your own database only, and let its journal carry the message out, so an order and its message can never be separated, and the only price is a message that may arrive twice. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Crash Debezium after sending one message, instead of two. Guess the counts first, and then run it. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
