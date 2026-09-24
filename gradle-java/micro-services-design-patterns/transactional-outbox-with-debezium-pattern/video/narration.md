# Transactional Outbox with Debezium Pattern — Video Narration Script

## 1. Transactional Outbox with Debezium

Hello, and welcome. This video explains the Transactional Outbox pattern in Java, using a real Postgres database, a real Kafka broker, and Debezium in between. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. When you have to save something and also tell others about it, do not do two separate things that can half happen. Save the message in your own database, beside the record, in the same single save, and let something else send it later. Now the same thing in our online store. When a customer checks out, the Orders service saves the order, and the rest of the shop must hear that the order was placed. So the service saves the order and an order placed message together, and a tool called Debezium sends the message on. By the end you will have seen an event sent for a row that was already deleted, a database keeping its log for a reader that was switched off, and the same event sent twice.

## 2. The Scenario

Here is the scenario. When a customer checks out, the Orders service saves the order in its own database. That database is Postgres. The rest of the shop, notifications, stock and shipping, hears about new orders through a message broker. That broker is Kafka. The shop wants three things. Every saved order is announced. Nothing is announced that was not saved. And each order's events, placed, paid and shipped, are heard in the order they happened.

## 3. Two Writes, One Crash

Act one, the two lines everybody writes first. There is no outbox yet. The checkout saves the order in Postgres, and then sends the event to Kafka itself. The process dies between the two. Order one is in Postgres. Kafka has no event. The customer is charged, and nobody is told. So swap the two lines. Send first, then save, and die in between. Now Kafka has one event, and order two is not in Postgres. The shop has announced an order that does not exist. Two systems, two steps, and no transaction that covers both.

## 4. Postgres's Words

Before the fix, some words, in plain language first. Picture an office where every piece of paper that touches any desk is first copied into a journal, automatically, by the building. Postgres has exactly that. Before it changes any table, it writes the change into a journal on disk, so that it can recover after a crash. Postgres calls it the write ahead log. Normally only Postgres reads it. But start Postgres with one setting, wal level logical, and an outside program can read the changes back as rows. That outside reader gets a bookmark in the journal, which Postgres calls a replication slot. And Postgres keeps every page of the journal that the reader has not yet confirmed.

## 5. Debezium's Words

Debezium is that outside reader. It holds the bookmark, is sent every committed change, and turns each one into a message. This is called change data capture. Its outbox event router takes each new row in the outbox table and makes one clean event out of it. The order id becomes the message key, and the row's id travels with the message as a label, which Kafka calls a header. Debezium also writes down how far through the journal it has read, and calls that its offset. Debezium usually runs in a program of its own. Here it runs inside the demo's own Java program, as a library, which Debezium calls the embedded engine. That saves a third container, and it reads the same journal in the same way.

## 6. One Transaction, And Debezium Sends

Act two, the pattern. Postgres runs with wal level logical. Debezium, version three point six point three, runs inside the program and holds its bookmark, the replication slot. The checkout now writes each order and a row in the outbox table, in one transaction, and commits. It has no Kafka code at all. Three orders, three outbox rows. Debezium reads the three commits from the journal and sends three events. Then order four writes both rows, the card is declined, and the whole transaction is rolled back. Order five commits after it. Kafka now holds four events, and not one for order four. The journal only hands over work that was committed, so an order and its event live or die together.

## 7. The Log, Not The Table

Act three is the headline of this video. This time each transaction writes the outbox row, and then deletes it again, before it commits. Three orders. The outbox table ends with no rows at all. And Kafka still receives three events. Debezium never looked at the table. It read the inserts from the journal, where they were written before the delete. A relay that reads the table, like the one in the plain-Java version, would have found nothing to send. Debezium itself recommends this way of working, because the outbox table then never needs cleaning.

## 8. Where Each Piece Lives

Here is where each piece lives, in words. The checkout writes to Postgres, and to nothing else. Postgres writes every change into its journal first, and keeps the journal for the slot. Debezium, inside the demo's program, is sent the committed outbox changes and forwards each one to Kafka, keyed by the order. Only after Kafka accepts an event does Debezium write down how far it has read. That order of steps matters, and act five shows why.

## 9. Debezium Is Down

Act four. Debezium is stopped, so the bookmark has no reader. The checkout does not notice. It takes three orders, and Kafka receives nothing. Meanwhile Postgres keeps every page of its journal that Debezium has not confirmed, and the amount it keeps for the slot grows. The setting that caps it is minus one, which means no cap at all. Debezium starts again, carries on from its bookmark, and sends all three: orders one, two and three. Nothing was lost, and nobody wrote a retry. Keep that minus one in mind. A Debezium that is switched off and forgotten makes Postgres keep its journal until the disk is full.

## 10. The Pattern In One Transaction

The whole pattern, on the checkout's side, is one transaction. Switch off automatic commits. Insert the order: order one, customer one, a total of two thousand nine hundred and ninety five pence, status placed. Insert the outbox row: its id is order one, slash, order placed. Its type is order placed, and its payload is the order. Then commit, once, for both rows. What matters most is what is missing. The checkout never opens a connection to Kafka. Debezium reads the committed rows from the journal.

## 11. Sent, But Not Written Down

Act five. Debezium sends orders one and two to Kafka, and then dies, before writing down how far it has read. Kafka holds two events. Debezium starts again, from the last place it wrote down. The slot still holds those two changes, because they were never confirmed, and hands them over again. Debezium sends both again. Four events for two orders. Each pair carries the same event id. Delivery is at least once. It is the price of writing down after sending, and the alternative, writing down first, would risk losing an event for good. The unchanging id is what lets a reader throw the second copy away.

## 12. Order Per Key, And The Bill

Act six. Three orders are placed, then paid, then shipped. Each step is its own transaction, and the orders take turns. Nine commits. Kafka splits the topic into three lanes that are read side by side. It calls them partitions. The order id picks the lane, and order is kept within a lane, never across lanes. Order one lands alone on partition one: placed, paid, shipped. Orders two and three share partition two, taking turns, and each keeps its own order. Then the bill. Two containers. Postgres started with wal level logical. And one replication slot, with no limit on what it keeps, so retiring Debezium means dropping the slot. The demo drops it, and the slot is gone.

## 13. What The Simulation Left Out

How does this compare with the plain-Java version earlier in the course? It got the whole pattern right. Both halves of the dual write failing, the message saved beside the order in one transaction, checkout carrying on while the sender is away, and the duplicate when the sender dies at the wrong moment. All of that holds here. What it left out is what a real database log adds. Debezium reads the log, not the table, so a deleted row is still sent. The slot keeps the log for its reader, with no limit. A rolled back transaction never appears at all. And order is kept per key, and only per key.

## 14. The Verdict

The verdict. Commit to one system only: the order and its outbox row, in one transaction. Let change data capture carry the message out, from the database's own log. Key each event by its order, so that one order's events stay in order. Watch the slot, and alert when it stops moving. Drop it when Debezium is retired. And make every reader of the topic forgive a duplicate, by remembering the event ids it has already handled.

## 15. What Is Real Here

What is real here? The database is Postgres, version eighteen point six, and the broker is Kafka, version four point three point one, each in a container that the demo starts at the beginning and stops at the end. Debezium is version three point six point three, the newest general release, running inside the demo, so there is no third container. The one thing you need is a container runtime, such as Docker Desktop, switched on before you start. Every number in this video comes from the program's own output, and two runs print the same thing. And when is this too much? If you cannot start your database with logical decoding, a relay that polls the outbox table on a timer gives the same guarantee, at the price of a table to clean.

## 16. Thanks for Watching

That's Transactional Outbox with Debezium. If you take one sentence away, take this one: commit to your own database only, and let its log carry the message out, so an order and its event can never part, and the only price is an event that may arrive twice. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, crash Debezium after sending one event instead of two, and predict the counts before you run it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
