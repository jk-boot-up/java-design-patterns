# Transactional Outbox with Debezium, Explained

## The pattern in one sentence

A transactional outbox writes each message as a row beside the record it is about, in the same database transaction, and leaves the sending to someone else — here Debezium, which reads the committed row out of the database's own log and sends it to Kafka.

## The analogy, before any of the tools' words

Think of the out-tray on a desk. You finish the paperwork for a sale and drop the letter in the tray in one movement, and somebody collects the tray later. The letter cannot go missing, because the moment the paperwork was filed the letter was already in the tray.

Now picture a building where every piece of paper that touches any desk is photocopied into a journal, automatically. The collector reads the journal, not the tray. You could drop the letter in the tray and throw it straight in the bin, and it would still go out. The building keeps every page of the journal the collector has not read yet, however long the collector is away. And a collector who posts a letter and is called away before ticking it off in the journal will post it again when they come back. Those three things are this project.

## What the tools call these things

The **write-ahead log**, or **WAL**, is Postgres's journal. Every change is written to it before any table is touched. With **`wal_level=logical`**, Postgres writes enough for an outside program to read the changes back as rows, and the decoder built into Postgres that does this is called **`pgoutput`**.

A **replication slot** is a bookmark Postgres keeps for one reader of the log. Postgres keeps every part of the log the reader has not confirmed. The setting that caps it, **`max_slot_wal_keep_size`**, is -1 by default: no cap.

**Debezium** is change data capture: it holds the slot and turns each committed change into a message. Its **outbox event router** turns each new outbox row into one event, with the order id as the message key and the row's id and type as headers. Debezium writes down how far it has read, its **offset**, and confirms it to the slot. Here it runs as the **embedded engine**, inside the demo's own program.

**Kafka** keeps messages in a **topic**, split into **partitions** that are read side by side. The message **key** picks the partition, and order is kept within a partition only.

## The six acts

### Two Writes, One Crash

With no outbox and no Debezium, the checkout saves the order in Postgres and sends the event to Kafka itself. It dies between the two. The order is saved and nobody hears of it. Swap the lines, send first, die before saving, and Kafka announces an order that does not exist.

```
  save, then send. the process dies in between. ORD-1 in Postgres: yes. events in Kafka: 0. the customer is charged and nobody is told.
  swap the lines: send, then save, and die in between. events in Kafka: 1. ORD-2 in Postgres: no. the shop announced an order that does not exist.
```

### One Transaction, And Debezium Sends

The pattern. Postgres runs with logical decoding, and Debezium holds the replication slot. The checkout writes each order and an outbox row in one transaction, and has no Kafka code at all. Debezium reads the three commits from the log and sends three events. Then ORD-4 writes both rows, the card is declined, and the transaction rolls back. ORD-5 commits after it. Kafka receives ORD-5 and nothing for ORD-4, because the log only hands over committed work.

```
  Postgres runs with wal_level logical. Debezium 3.6.3.Final runs inside this program and holds replication slot orders_outbox. slot active: yes.
  the checkout writes each order and an outbox row in one transaction, and has no Kafka code at all. orders: 3, outbox rows: 3.
  Debezium reads the 3 commits from Postgres's log and sends them. events in Kafka: 3.
  events in Kafka: 4. events for ORD-4: 0. the log only hands over committed work, so the order and its event live or die together.
```

### The Log, Not The Table

This is the headline find. Each transaction writes the outbox row and deletes it again before committing. The table ends with no rows. Kafka still receives all three events, because Debezium read the inserts from the log. A relay that polls the table would have had nothing to send.

```
  orders: 3. outbox rows: 0. events in Kafka: 3.
```

### Debezium Is Down

Debezium stops and lets go of the slot. The checkout takes three orders anyway. The log Postgres keeps for the slot grows, and the limit is -1, which means none. Debezium starts again, carries on from the slot, and sends all three. Nothing was lost and nobody wrote a retry. The same property is a danger: a slot nobody reads keeps the log for ever.

```
  Debezium is stopped. slot active: no. the checkout still takes 3 orders. orders: 3. events in Kafka: 0.
  the slot makes Postgres keep every part of the log Debezium has not confirmed. log kept for the slot: grew while it was down. limit: -1, which means none.
  Debezium starts again, carries on from its slot, and sends 3: ORD-1, ORD-2, ORD-3. nothing was lost and nobody wrote a retry.
```

### Sent, But Not Written Down

Debezium sends ORD-1 and ORD-2, then dies before writing down how far it has read. It starts again from the last place it wrote down and sends both again. Four events for two orders, each pair carrying the same event id. Delivery is at least once.

```
  Debezium sends ORD-1 and ORD-2 to Kafka, then dies before writing down how far it has read. events in Kafka: 2. slot active: no.
  it starts again from the last place it wrote down, and sends both again. events in Kafka: 4 for 2 orders.
  ORD-1/OrderPlaced arrived 2 times, ORD-2/OrderPlaced arrived 2 times, with the same event id each time. delivery is at least once.
```

### Order Per Key, And The Bill

Three orders are placed, paid and shipped, each step its own transaction, the orders taking turns. Each order's three events land on one partition, in the order they were committed. ORD-1 is alone on partition 1; ORD-2 and ORD-3 share partition 2 and interleave. Across orders, nothing is promised. The bill: two containers, Postgres started with logical decoding, one slot that must be dropped when Debezium is retired, and readers that must recognise an event id they have already seen.

```
  ORD-1: partition 1, OrderPlaced, OrderPaid, OrderShipped.
  ORD-2: partition 2, OrderPlaced, OrderPaid, OrderShipped.
  ORD-3: partition 2, OrderPlaced, OrderPaid, OrderShipped.
  partition 0 holds none, partition 1 holds only ORD-1, partition 2 holds ORD-2 and ORD-3 taking turns. the order id is the key, and the key picks the partition.
  the bill: 2 containers, Postgres started with wal_level logical, and 1 replication slot.
  a slot whose reader has gone keeps log for ever: limit -1. retiring Debezium means dropping its slot. slot exists now: no.
```

## The verdict

Commit to one system only. Let the database's own log carry the message out. Pay for it with a slot to watch and a reader that forgives duplicates.
