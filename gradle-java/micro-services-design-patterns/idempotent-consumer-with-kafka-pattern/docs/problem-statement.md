# Problem Statement

## The scenario

When a customer places an order, checkout writes an OrderPlaced message to a Kafka topic and goes back to selling. The notifications service reads the topic and queues one confirmation email for each order, as a row in its own Postgres database. Several copies of the notifications service run at once, and they are restarted whenever a new version is deployed. The shop wants exactly one email per order: none missing, and none sent twice.

## The naive version

A copy that reads each order and queues its email, and remembers nothing. It is correct on every day when no copy stops.

```
  notifications copy A is handed 3, queues 3 confirmation emails, and crashes before writing down its place. place written down: none.
  copy B joins the same group and is handed the same orders again, at places 0, 1, 2. nothing on them says they are repeats.
  deliveries: 6 for 3 orders. confirmation emails queued: 6.
```

## What the plain-Java project already did

The plain-Java Idempotent Consumer project in this course taught the whole idea. It showed a message arriving twice, a set of ids in memory catching the duplicate and then losing everything at a restart, a crash between the work and the id sending the email twice, and the fix: the id and the work written in one transaction. It showed a handler that needs none of this, and the expiry window a dedupe store has to choose. Nothing here replaces it.

It had one comfort, though. Its broker called the same consumer object twice, one call after the other, on one thread. So a duplicate always came to a consumer that had already finished with the first delivery, and it could come to the same memory. And its restart and its crash were stand-ins: a set emptied, an exception thrown.

## What this project must deliver

The same shop and the same emails, with the orders moved into a real Kafka topic and the ids into a real Postgres table, both in containers the demo starts and stops. A copy that crashes before writing down its place, and Kafka handing every order again to the next copy, with no mark on them. A set of ids in memory that never sees the duplicate, because the duplicate goes to a copy with an empty set. The table, written in the same transaction as the email, turning six deliveries into three emails. A crash between two steps, and a crash inside one transaction. Two copies holding the same order at the same time, with Postgres deciding which one queues the email and Kafka refusing the loser's bookkeeping. And a replay after a cleanup that kept the ids for less time than Kafka kept the orders.

Every figure printed is the tools' own, and two runs back to back print the same thing.
