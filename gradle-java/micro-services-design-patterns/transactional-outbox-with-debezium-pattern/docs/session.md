# Session Guide — Transactional Outbox with Debezium Pattern

A 60-minute session built around one question: if the Orders service is only allowed to commit to its own database, how does the rest of the shop reliably hear about every order?

## Learning Objectives

1. Say, in plain words, what the write-ahead log, logical decoding, a replication slot, Debezium's offset and the outbox event router are.
2. Show both halves of the dual-write failure against a real database and a real broker.
3. Explain why a rolled-back checkout publishes nothing, and why a deleted outbox row is still published.
4. Explain what a replication slot does while Debezium is down, and why a forgotten slot is dangerous.
5. Explain why delivery is at least once, and how the event id and the message key help the reader.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The out-tray and the journal, and the plain-Java version recapped in two minutes |
| 0:08–0:18 | Act one: two writes, one crash |
| 0:18–0:30 | Acts two and three: one transaction, and the log, not the table |
| 0:30–0:42 | Acts four and five: Debezium down, and sent but not written down |
| 0:42–0:52 | Act six: order per key, and the bill |
| 0:52–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd micro-services-design-patterns/transactional-outbox-with-debezium-pattern
./gradlew -q run
```

Act one: which of the two failures would a customer notice first, and which would support notice first? Act two: ORD-4 wrote an outbox row; why did nothing reach Kafka? Act three: the table holds 0 rows; where did Debezium find the three events? Act four: the checkout kept working with Debezium stopped; what was Postgres doing on its behalf? Act five: why were two events sent twice, and what is the same on both copies? Act six: why are ORD-2 and ORD-3 on the same partition, and does it matter?

Then open `src/main/java/com/jk/explore/transactionaloutboxdebezium/OutboxCheckout.java` and read `place` aloud. Notice what is missing: there is no Kafka import in the file. Then open `ChangeDataCapture.java` and read `handleBatch`: send first, write down second — the whole at-least-once story in two lines.

## Discussion

Ask the room why Debezium writes down its position after Kafka accepts the event, and not before. Before, and a crash in between loses the event for good. After, and a crash in between is act five: a duplicate. The pattern chooses the duplicate.

Then ask who should be paged when the slot stops moving, and what happens to the database's disk over a long weekend if nobody is.

## Exercises

1. In `OutboxCheckout`, move the outbox insert into its own transaction after the order's. Crash between them, and count orders and events.
2. Set `max_slot_wal_keep_size` to a small value when starting Postgres, stop Debezium, place many orders, and look at `wal_status` in `pg_replication_slots`.
3. Change the router so the key is the customer rather than the order. Predict which events share a partition.
4. In act five, crash after sending 1 instead of 2. Predict the counts.
5. Write a reader of `order-events` that keeps the ids it has seen in a table, and run act five into it. Count the emails.

Close with the verdict: commit to one system only, let the log carry the message out, and make every reader forgive a duplicate.
