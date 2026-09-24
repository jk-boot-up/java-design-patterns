# Session Guide — Idempotent Consumer with Kafka Pattern

A 60-minute session built around one question: when Kafka hands the same order out twice, and to a different copy of the service, what has to be true for the customer to get exactly one email?

## Learning Objectives

1. Say, in plain words, what a topic, an offset, a consumer group, committing an offset, the patience limit and retention are.
2. Show why a copy that stops before committing its offset makes Kafka hand the same orders to the next copy, with no mark on them.
3. Explain why a set of ids in memory never sees a Kafka redelivery.
4. Explain why the id and the work must be in one transaction, with the counts from act four.
5. Explain how the primary key, not a check in Java, decides between two copies holding the same order, and why the cleanup window must be at least the topic's retention.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The cloakroom analogy, and the plain-Java version recapped in two minutes |
| 0:08–0:18 | Acts one and two: Kafka sends it again, to a copy with an empty memory |
| 0:18–0:30 | Acts three and four: the table, and where the crash lands |
| 0:30–0:42 | Act five: two copies at once |
| 0:42–0:52 | Act six: the bill, and the verdict |
| 0:52–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd micro-services-design-patterns/idempotent-consumer-with-kafka-pattern
./gradlew -q run
```

Act one: copy A handled all three orders, so why did the broker hand them out again? Act two: copy A's set held 3 ids; why did it not help? Act three: what did copy B actually do for each of the three orders? Act four: both halves crash copy A at almost the same line; why is one two emails and the other one? Act five: why did copy B wait, and what would have happened with no primary key? Act six: who chose 24 hours, and who chose 168?

Then open `src/main/java/com/jk/explore/idempotentconsumerkafka/RecordIdInSameTransaction.java` and read `begin` aloud. The whole pattern is one insert with `on conflict do nothing`, a look at how many rows it wrote, and the email written in the same transaction.

## Discussion

Ask the room where to commit the Kafka offset: before the database transaction, or after it. Before, and a crash in between loses the email for good — the bookmark has moved past an order nobody handled. After, and a crash in between is act three: a redelivery the table absorbs. The pattern only works one way round.

Then ask what the email provider does. The table can promise one row in `confirmations`; it cannot promise one email leaves the building, because the provider is outside the transaction. That is where an outbox, and the provider's own idempotency key, come in.

## Exercises

1. Turn on `enable.auto.commit` in `Notifications` and run act one. Predict how many orders copy B is handed.
2. Remove the primary key from `handled_messages` and replace the insert with a select followed by an insert. Run act five and count the emails.
3. Key the table on the offset instead of the message id, then have checkout place ORD-1 twice. Count the emails.
4. Set the cleanup window in act six to 168 hours, and predict the last count.
5. In act one, leave copy A open instead of closing it. Find out which of Kafka's two limits — the heartbeat's 45 seconds, or the patience of five minutes — decides when copy B is handed the orders.

Close with the verdict: one table, the id as its key, written first in the same transaction as the work, and the offset committed only after.
