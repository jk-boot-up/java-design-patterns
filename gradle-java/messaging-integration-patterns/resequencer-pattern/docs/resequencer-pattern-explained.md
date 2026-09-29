# Resequencer, Explained

## The pattern in one sentence

A resequencer holds messages that arrive early and releases each sequence
strictly in order, giving up on a gap after a limit.

## The 5 acts

### 1. Applied as they arrive

The five updates for ORD-1 arrive as #1, #3, #2, #5, #4. The order page
applies each as it comes: the customer sees PLACED, PACKED, PAID, DELIVERED,
SHIPPED, and the page ends on SHIPPED although the parcel was delivered.

### 2. A resequencer

A `Resequencer` in front of the page releases each update only when it is the
next number expected. The customer now sees the statuses in their true order,
and the page ends on DELIVERED.

### 3. Hold and release

The trace shows the resequencer at work. #1 is released at once. #3 arrives
early and is held. When #2 arrives, it is released, followed by the held #3.
#5 is held until #4 arrives, and then both are released.

### 4. One sequence per order

Every order has its own sequence and its own buffer. Updates for ORD-2 and
ORD-3 arrive mixed together; each order's updates are released in that
order's own sequence, without waiting for the other.

### 5. The bill

For ORD-4, update #3 is lost. #4 arrives and is held; the page still says
PAID. When #5 arrives, two updates are waiting, which is this resequencer's
limit, so it gives up on #3 and releases #4 and #5: the page shows DELIVERED,
and PACKED is never shown. Without a limit, the page would wait for ever.

## The verdict

Use a resequencer when order matters and delivery cannot guarantee it. Number
messages per key, bound the buffer, decide what to do about gaps, and prefer a
transport that keeps order per key when you can choose one.

## How to recognise this in code you did not write

- Sequence numbers or versions on messages for one entity.
- A buffer keyed by entity with a next-expected counter.
- `resequence` in Camel routes.

## Where you have already met this

- Apache Camel's `resequence`.
- TCP, which puts network packets back in order using sequence numbers.
- Kafka's ordering per partition key, which avoids the need.
