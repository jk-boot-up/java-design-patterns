# Problem Statement

## The scenario

When a customer checks out, the Orders service saves the order in its own Postgres database. The rest of the shop — notifications, stock, shipping — learns about it from an OrderPlaced event on a Kafka topic. The shop wants every saved order announced, no announcement for an order that was not saved, and every order's events heard in the order they happened.

## The naive version

Two lines: save the order, then send the event. It is correct on every day when the process does not stop between them.

```
  save, then send. the process dies in between. ORD-1 in Postgres: yes. events in Kafka: 0. the customer is charged and nobody is told.
  swap the lines: send, then save, and die in between. events in Kafka: 1. ORD-2 in Postgres: no. the shop announced an order that does not exist.
```

## What the plain-Java project already did

The plain-Java Transactional Outbox project in this course taught the whole idea. It showed both halves of the dual-write failure, the outbox row written in the same transaction as the order, a relay that sends the rows later, checkout carrying on through a broker outage, and the duplicate that comes from a relay dying after sending and before marking the row sent. Nothing here replaces it.

It had one comfort, though. Its relay read the table, its database was a map, and its broker was a list. There was no log for anyone to read, no bookmark for the database to keep, and only one list, so everything arrived in the order it was written.

## What this project must deliver

The same shop and the same orders, with the orders and the outbox in a real Postgres started with logical decoding, the events in a real Kafka topic with three partitions, and the relay replaced by Debezium reading Postgres's write-ahead log. Both halves of the dual write failing against the real tools. The outbox committed with the order and published by Debezium, with a rolled-back checkout publishing nothing. An outbox row deleted in its own transaction and still published. Debezium stopped, the slot keeping the log, and every order caught up on restart. Debezium dying between sending and writing down its position, and the same events sent again with the same ids. And each order's events on one partition, in commit order.

Every figure printed is the tools' own, and two runs back to back print the same thing.
