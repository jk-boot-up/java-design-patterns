# Backpressure, Explained

## The pattern in one sentence

Backpressure lets a slow consumer control how fast a producer sends, so
waiting work stays bounded instead of filling memory.

## The 5 acts

### 1. No backpressure

The supplier pushes as fast as it can and the indexer buffers everything it
has not reached yet. After ten seconds, a thousand are indexed and nine
thousand are waiting in memory, a pile that grows by nine hundred every
second. A bigger feed, or a slower indexer, and the service runs out of memory.

### 2. A bounded buffer

The buffer now holds at most five hundred products. When it is full, the
supplier has to wait for space. Memory stays flat, never more than five
hundred waiting, and all ten thousand products are indexed in a hundred
seconds, the indexer's own pace.

### 3. Ask for what you can handle

Instead of the producer pushing, the consumer pulls. Using Java's own `Flow`
interfaces, the indexer calls `request(10)`, indexes those ten, then asks for
ten more. The publisher never sends anything it was not asked for, so at most
ten products are ever in flight.

### 4. Keep only the latest

Some data does not need every value. A warehouse sends a thousand stock-level
updates for ten products. The consumer only needs the current level, so a
conflator keeps one pending value per product and drops the older ones: ten
updates are delivered, the latest for each.

### 5. The bill

Backpressure does not make the work faster; it moves the waiting upstream. The
supplier's feed took a hundred seconds instead of ten, so the supplier must
be able to cope with being slowed. And dropping is only safe for data where
the latest value is all that matters, never for orders or payments.

## The verdict

Use backpressure wherever a fast source can outrun a slow sink for long:
bound every buffer, prefer consumers that pull, and drop only data where the
latest value is enough. Make sure the producer can cope with being slowed.

## How to recognise this in code you did not write

- `Flow.Subscriber` calling `subscription.request(n)`.
- Bounded queues whose `put` blocks, or `offer` that returns false.
- Operators named `onBackpressureBuffer`, `onBackpressureDrop` or `onBackpressureLatest`.

## Where you have already met this

- `java.util.concurrent.Flow` and `SubmissionPublisher`.
- Project Reactor, RxJava, Akka Streams and Kafka consumers pulling at their own pace.
- A bounded `ArrayBlockingQueue`, whose `put` waits when it is full.
- TCP flow control, which slows the sender when the receiver's window is full.
