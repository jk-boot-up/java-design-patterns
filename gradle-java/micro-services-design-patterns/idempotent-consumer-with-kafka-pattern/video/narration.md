# Idempotent Consumer with Kafka Pattern — Video Narration Script

## 1. Idempotent Consumer with Kafka

Hello, and welcome. This video explains the Idempotent Consumer pattern in Java, using a real Kafka broker and a real Postgres database. This video is presented by Jayasekhar Konduru. First, a simple definition. A message can arrive more than once. So the receiver writes down the I D of every message it handles, in the same step as the work itself. When a message arrives whose I D is already written down, it does nothing. In our online store, every time a customer places an order, checkout sends a message. The notifications service then queues one confirmation email. If that message arrives twice, the customer must still get exactly one email. By the end, you will hear Kafka hand the same three orders to a second copy of the service. A list of I Ds in memory fail to notice. And two copies working on the same order at once, with the database deciding which one wins.

## 2. The Scenario

Here is the scenario. When a customer places an order, checkout sends a message saying so. The notifications service reads each message. And it queues one confirmation email, as a row in its own database. Several copies of the notifications service run at the same time. And every time a new version is released, they are stopped and started again. The shop wants exactly one email per order. None missing, and none sent twice.

## 3. Kafka's Words

Before the demo, a few words, in plain language. Picture a shared notebook. The till writes one line in it for every sale. And the back office reads down it, with a bookmark. In Kafka, the notebook is called a topic. Every message sits at a numbered place in it, counting from zero. That number is called the offset. A service reading the topic is called a consumer group, however many copies of it are running. Kafka keeps each group's bookmark: the place it has reached. A copy must ask for the bookmark to be moved. That is called committing the offset. Until it is moved, Kafka assumes nothing after it was handled.

## 4. Kafka Sends It Again

First demo: Kafka sends it again. Checkout places three orders, and Kafka puts them at places zero, one, and two. Copy A of the notifications service is handed all three. It queues three confirmation emails. Then it crashes, before asking Kafka to move the bookmark. So Kafka has no bookmark for the group at all. Copy B joins the same group. And Kafka hands it the same three orders again, at the same places. Nothing on them says they are repeats. Kafka has no such mark. Six deliveries, for three orders. And six emails. This is what Kafka means by at least once.

## 5. A List Of Ids In Memory

Second demo: a list of I Ds in memory. Copy A now keeps a list of the I Ds it has handled, in its own memory. It handles three orders, remembers three I Ds, and crashes before moving the bookmark. Copy B is handed the same three orders. Its list starts empty. So it queues all three emails again. Six emails. This is the most important finding in the video. On Kafka, an order is only handed out again because a copy stopped. So the repeat always lands on a copy with fresh, empty memory. A list in memory never even sees the duplicate it was meant to catch.

## 6. Postgres's Words

The fix needs three database words, in plain language. A group of changes that are kept together, or thrown away together, is called a transaction. Nothing in it is visible to anyone else until it is committed. A column that no two rows may share is called a primary key. And when two writers try to write the same key at the same moment, the database makes the second one wait. That waiting is caused by a lock.

## 7. A Table, One Transaction

Third demo: the pattern. Copy A writes each order's I D into a table of handled messages. The I D is the primary key. And the email is written beside it, in the same transaction. Then copy A crashes, before moving the bookmark. Copy B is handed the same three orders. For each one, it tries to write the I D. And Postgres says the I D is already there. So copy B skips all three, and queues no emails. Six deliveries, three emails, and three I Ds. The table outlived the copy that wrote it.

## 8. Where The Memory Lives

Here is the whole setup, in words. Kafka keeps the orders, and each group's bookmark. A copy of the service is handed orders, starting from the bookmark. For each order, it opens one database transaction. It writes the I D first, then the email, and commits. Only after that does it ask Kafka to move the bookmark. If it crashes before the bookmark moves, the order goes out again, to another copy. And the I D is already waiting for it. The I D and the email are saved together, or not at all.

## 9. Where The Crash Lands

Fourth demo: where the crash lands. First, the I D is written after the email, as a separate step. Copy A queues the email for order one. Then it crashes before writing the I D. One email, and no I D. Copy B is handed the order, finds no I D, and queues the email again. Two emails, for one order. Now the I D and the email go in one transaction. Copy A crashes before the commit. Its connection drops, and Postgres throws the whole transaction away. No email, and no I D. Copy B handles the order properly: one email, one I D. Exactly once, from a broker that only promises at least once.

## 10. The Pattern In Two Statements

In the code, the whole pattern is two statements and a commit. The copy opens a transaction, and inserts the message I D. It asks Postgres to write nothing if the I D is already there. Postgres answers with how many rows it wrote. One row means the order is new. So the email is queued, in the same transaction. Zero rows means it was already handled. Then the transaction commits. And only then does the copy ask Kafka to move the bookmark.

## 11. Two Copies At Once

Fifth demo, and this is something the plain Java version could never show. Kafka gives every copy a patience limit. It is how long a copy may go without asking for more orders, before Kafka decides it is stuck. By default it is five minutes. Here, it is three seconds. Copy A is handed order one. It writes the I D and the email, but is slow to commit. After three seconds, Kafka hands the same order to copy B. Now two copies are working on one order. Copy B tries to write the same I D. And Postgres makes it wait, on copy A's lock. Copy A commits. Postgres tells copy B the I D is taken, so copy B skips it. One email. Then copy A asks Kafka to move the bookmark, and Kafka refuses. Copy A no longer owns that order. A check done in Java would have let both copies through. Only the database's primary key could decide.

## 12. The Bill

Sixth demo: the bill. The table cannot keep every I D forever. So a clean-up job deletes old ones. Three orders placed two days ago are handled, and their three I Ds stored. The clean-up keeps I Ds for one day. So it deletes all three. But a topic also keeps its orders for a set time. This one keeps them for seven days, which is Kafka's default. An operator moves the group's bookmark back to the start, to replay it. Three orders are handed out again. Their I Ds are gone, so three more emails are queued. Six in total. So keep the I Ds at least as long as Kafka keeps the orders. And there are two more systems to run, a broker and a database, for one email per order.

## 13. What The Simulation Left Out

How does this compare with the plain Java version? It got the whole pattern right. The list in memory that is lost on restart. The crash between the work and the I D. And the single transaction that fixes both. All of that holds here. What it left out is what Kafka adds. The repeat goes to a different copy, with no mark on it. Two copies can hold the same order at the same moment. And the clean-up window is no longer a free guess. How long the topic keeps messages sets its minimum.

## 14. The Verdict

So, here is the verdict. Behind Kafka, assume every message will be handed out twice, to a different copy. Keep the I Ds in a table, in the same database as the work. With the I D as the primary key. Write the I D first, inside the same transaction as the work. Let the database's answer decide whether to carry on. Commit the transaction, and only then move the bookmark. And keep the I Ds at least as long as the topic keeps the messages.

## 15. What Is Real Here

A quick, honest note about this demo. The broker is Kafka, version four point three point one. The database is Postgres, version eighteen point six. Both are the newest releases. Each runs in a container that the demo starts and stops by itself. You just need Docker switched on first. Every number you heard comes from the program's own output. So, when is this too much? If the work is naturally safe to repeat, like setting an order's status to shipped, there is nothing to guard against. And no table is needed.

## 16. Thanks for Watching

That's Idempotent Consumer, with Kafka. If you remember one sentence, make it this one. Kafka will hand the same order to two copies, one after a crash or both at once, and only an I D written in the same transaction as the work catches both. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Remove the primary key from the table of handled I Ds. Run the fifth demo, and count the emails. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
