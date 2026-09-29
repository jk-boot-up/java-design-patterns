# Event-Carried State Transfer with Kafka, Explained

## The pattern in one sentence

With Kafka, state events keyed by entity on a compacted topic let any service
build and keep its own copy, in order, with deletions as tombstones.

## The 5 acts

### 1. Thin events and call-backs

The customer service publishes events to Kafka that say only that a customer
changed. Shipping reads ten of them, but still has to call the customer
service for every label: a hundred labels, a hundred calls. When the customer
service is down, not one label is printed.

### 2. The address in the event

Now each event carries the address, keyed by customer, on a compacted topic.
Shipping reads the topic into its own copy: ten addresses. With the customer
service still down, all hundred labels are printed, with no calls at all.

### 3. A new copy from the topic

Customer C1 moves to York. A new shipping instance starts with nothing and
reads the topic from the beginning: eleven events for ten customers, and the
latest event for C1 wins, so its label goes to York. The old copy, which has
not read the new event yet, still says Leeds: copies lag until they read.

### 4. Order within a partition

Customer C2 moves to Hull, then Bristol. Sent without a key to two different
partitions, and read partition 1 first, the older address, Hull, ends up in
the copy. Kafka only keeps order within a partition. Keyed by customer, both
events land on the same partition in order, and the copy ends on Bristol, with
no version numbers needed.

### 5. Deleting is an event

Customer C3 closes the account. The customer service sends a tombstone: an
event for C3 with no value. A copy built from the topic now holds nine
addresses, and C3 has no label. Every service holding a copy must read and
honour tombstones, or the address lives on; and the topic and every copy are
more data to store, secure and keep in step.

## The verdict

Carry state on a compacted, keyed Kafka topic when many services need the
data and must work when its owner is down. Key by entity, honour tombstones,
and copy only the fields each service needs.

## How to recognise this in code you did not write

- Topics with `cleanup.policy=compact`.
- Events keyed by an entity's identifier.
- Null-valued events used as deletes.

## Where you have already met this

- Compacted Kafka topics used as the source of a service's local table.
- Kafka Streams `KTable`s, which are exactly this local copy.
- Change data capture with Debezium, publishing every row change.
