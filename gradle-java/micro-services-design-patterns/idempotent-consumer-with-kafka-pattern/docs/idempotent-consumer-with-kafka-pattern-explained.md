# Idempotent Consumer with Kafka, Explained

## The pattern in one sentence

An idempotent consumer writes down the id of every message it has handled, in the same transaction as the work, so that when the same message arrives again it can see it has been done and do nothing.

## The analogy, before any of the tools' words

Think of a cloakroom attendant with a ticket book. Every coat handed over has a ticket number, and the attendant writes the number in the book as the coat goes on the rail. If somebody comes back with the same ticket and says their coat was never taken, the attendant looks in the book, finds the number, and does not hang a second coat.

Now three things a real cloakroom has to get right, which the plain-Java project in this course could mostly skip. First, the attendant who sees the repeat is usually not the one who took the coat: repeats turn up after a change of shift. So the book has to stay behind the counter, not go home in someone's pocket. Second, the number has to go in the book at the same moment the coat goes on the rail. Third, two attendants may be handed the same ticket at the same moment, and only one of them may hang the coat. Those three are the whole of this project.

## What Kafka and Postgres call these things

A **topic** is a list of messages that is only ever added to. Checkout writes one OrderPlaced message to it per order. Every message sits at a numbered place, counting from 0, and Kafka calls that number the **offset**.

A **consumer group** is one service, however many copies of it run. Here the group is the notifications service, and its copies are called copy A and copy B.

**Committing the offset** is a copy asking the broker to write down the place the group has reached — the bookmark. The copies in this project commit by hand, only after the work, and that makes delivery **at least once**: a copy that stops before committing leaves the orders to be handed out again.

**`max.poll.interval.ms`** is Kafka's patience: how long a copy may go without asking for more before the broker decides it is stuck and hands its orders to another copy.

**Retention** is how long a topic keeps its messages. A **replay** is an operator moving a group's bookmark back so it reads them again.

In Postgres, a **transaction** is a group of changes kept together or thrown away together. A **primary key** is a column no two rows may share, and a **lock** is how Postgres makes a second writer of the same key wait for the first.

## The six acts

### Kafka Sends It Again

Checkout places 3 orders, at places 0, 1 and 2. Copy A is handed all 3, queues 3 emails, and crashes before committing. The broker has written down no place for the group. Copy B joins the group and is handed the same 3 orders at the same places, 0, 1 and 2. Nothing on them says they are repeats: Kafka has no such mark. Six deliveries for three orders, and six emails.

```
  a Kafka broker and a Postgres database are running in containers. checkout places 3 orders, at places 0, 1, 2.
  notifications copy A is handed 3, queues 3 confirmation emails, and crashes before writing down its place. place written down: none.
  copy B joins the same group and is handed the same orders again, at places 0, 1, 2. nothing on them says they are repeats.
  deliveries: 6 for 3 orders. confirmation emails queued: 6.
```

### A List Of Ids In Memory

This is the headline find. Copy A keeps a set of handled ids in its own memory. It handles 3 orders, remembers 3 ids, and crashes before committing. Copy B is handed the same 3, and its set starts with 0 ids. Six emails again. The set was never going to help: Kafka hands an order out again only because a copy stopped, so the repeat always lands on a copy whose memory is new.

```
  copy A keeps a list of handled ids in memory. it handles 3 orders, remembers 3 ids, and crashes before writing down its place.
  copy B is handed the same 3. its list starts with 0 ids. confirmation emails queued: 6.
  the list died with copy A. a redelivery happens because a copy stopped, so it always lands on a list that is new.
```

### A Table Of Ids, In The Same Transaction

The pattern. Copy A writes each order's id into the handled-messages table and its email into the confirmations table, in one transaction, and commits. Then it crashes before committing its place in Kafka. Copy B is handed the same 3 orders. For each one it tries to write the id, and Postgres says the id is already there, so B skips all 3 and queues none. Six deliveries, three emails, three ids. The table outlived the copy that wrote it.

```
  copy A writes each order's id and its email in one database transaction. it handles 3 and crashes before writing down its place.
  copy B is handed the same 3. the table already holds their ids, so B skips 3 and queues 0.
  deliveries: 6. confirmation emails queued: 3. ids stored: 3. the table outlived the copy that wrote it.
```

### Where The Crash Lands

First the id is written after the email, as a second step. Copy A queues ORD-1's email and dies before writing the id: one email, no id. Copy B is handed ORD-1, finds no id, and queues the email again. Two emails for one order.

Then the id and the email go in one transaction, and copy A dies before the commit. Its database connection drops, and Postgres throws the whole transaction away: no email, no id. Copy B is handed ORD-1 and handles it properly: one email, one id. Exactly once, from a broker that only promises at least once.

```
  id written after the email, as a second step. copy A queues ORD-1's email and dies before writing the id. emails: 1, ids: 0.
  copy B is handed ORD-1, finds no id, and queues it again. emails for ORD-1: 2.
  id and email in one transaction. copy A dies before the commit, and Postgres throws both away. emails: 0, ids: 0.
  copy B is handed ORD-1 and handles it properly. emails: 1, ids: 1. exactly once, from a broker that promises at least once.
```

### Two Copies At Once

Kafka's patience is set to 3 seconds for this act. Copy A is handed ORD-1, starts its transaction, writes the id and the email, and then is slow: it does not commit, and it does not ask Kafka for more. After 3 seconds Kafka decides A is stuck and hands ORD-1 to copy B. Now both copies are working on the same order. B tries to write the same id, and Postgres makes B wait, because A holds a lock on that key. A commits. Postgres tells B the id is taken, and B skips it. One email. Then A asks Kafka to commit its place, and Kafka refuses with a `CommitFailedException`: A no longer owns those orders.

A check done in Java — "is the id in the table? if not, carry on" — would have answered "not there" to both copies, because A had not committed. Only the database's own rule about the key could decide.

```
  copy A is handed ORD-1 and is slow. after 3 seconds without asking for more, Kafka decides A is stuck and hands the order to copy B.
  both copies are working on ORD-1. A has written the id and not committed. B writes the same id, and Postgres makes it wait. sessions waiting on a lock: 1.
  A commits. B is told the id is taken, and skips it: queued by B: 0. emails for ORD-1: 1.
  A finishes and asks for its place to be written down. Kafka refuses with CommitFailedException: A no longer owns those orders.
```

### The Bill

Three orders placed two days ago are handled, and their 3 ids stored. A cleanup job keeps ids for 24 hours, and deletes all 3. This topic keeps orders for 168 hours, Kafka's default of seven days. An operator replays the group from the start, and 3 orders are handed out again. With their ids gone, 3 more emails are queued: 6 in all. The window for keeping ids is not a free choice: it must be at least as long as Kafka keeps the orders.

Two more costs follow. Every message needs an id that stays the same when it is sent again, and every copy needs a database transaction to put it in. And there are two more systems to run: 2 containers, a broker and a database, for 1 email per order.

```
  3 orders placed two days ago are handled. ids stored: 3. a cleanup job keeps ids for 24 hours, and deletes 3.
  this topic keeps orders for 168 hours. an operator replays the group from the start. handed again: 3. emails queued: 6.
  keep the ids at least as long as Kafka keeps the orders.
  and every message needs an id that stays the same when it is sent again, and every copy needs a transaction to put it in.
  and there are two more systems to run: this demo needed 2 containers, a broker and a database, for 1 email per order.
```

## The verdict

Behind Kafka, assume every message will be handed out twice, and to a different copy. Keep the ids in a table in the same database as the work, with the id as the primary key. Write the id first, inside the same transaction as the work, and let the database's answer decide whether to go on. Commit the transaction, then commit the offset. Keep the ids at least as long as the topic keeps the messages.

## How to recognise this in code you did not write

- A Kafka consumer with automatic offset commit left on (`enable.auto.commit` is on by default). The bookmark moves on a timer, whether the work is done or not.
- A `Set<String>` of seen ids in a consumer's field. It will be empty on the only copy that ever sees a repeat.
- A dedupe check that reads the table, then inserts in a separate step, with no primary key on the id. Two copies at once will both pass the check.
- The id recorded after the work, in a second transaction or in a different store such as a cache.
- A dedupe keyed on the offset instead of a message id. The same message sent twice lands at two offsets.
- A cleanup job whose window nobody has compared with the topic's `retention.ms`.

## Where you have already met this

Email and notification senders, payment handlers, stock reservation services, search indexers: anything that reads a Kafka topic and changes something outside Kafka. Spring Kafka and most outbox relays make the same at-least-once promise. The same table and the same transaction work behind RabbitMQ, Amazon SQS or any broker that redelivers.

## When this is too much

If the work is naturally safe to repeat — set the status to shipped, set the stock to twenty — no table is needed. If the work lives outside the database, the table cannot share its transaction, and an outbox has to carry the work instead. And the table grows by one row per message, so somebody owns its cleanup.
