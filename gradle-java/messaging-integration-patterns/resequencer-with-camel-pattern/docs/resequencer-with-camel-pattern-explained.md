# Resequencer with Apache Camel, Explained

## The pattern in one sentence

With Camel, a resequencer is one `resequence()` step that restores order by
sequence number, either as a stream with a gap timeout or in sorted batches.

## The 5 acts

### 1. Applied as they arrive

Without a resequencer, updates are applied in arrival order: #1, #3, #2, #5,
#4. The customer sees placed, packed, paid, delivered, then shipped, and the
page ends on SHIPPED although the parcel was delivered.

### 2. Stream mode

`resequence(header("seq")).stream()` releases each update as soon as all the
earlier ones have been seen. The page shows placed, paid, packed, shipped,
delivered. One surprise: the first update appeared only after about 0.3
seconds, the timeout, because Camel cannot know that #1 is the first.

### 3. Batch mode

Batch mode collects a group of five, sorts it, and releases it together.
After four arrivals the page shows nothing at all. When the fifth arrives,
all five appear at once, in order. Batch mode never shows anything out of
order, but the customer waits for the whole group.

### 4. Two orders at once

Updates for two orders arrive interleaved. Camel's stream mode keeps one
sequence for everything, so it cannot keep two orders apart. Batch mode,
sorting by order and then number, releases ORD-2's placed and paid, then
ORD-3's placed, paid and packed.

### 5. The bill

Update #3 is lost. #4 and #5 arrive and wait, and the page stays on PAID.
After about half a second, the timeout, Camel gives up on #3 and releases the
rest: the page says DELIVERED. A short timeout gives up on a late message
quickly; a long one leaves the customer on an old status for longer.

## The verdict

Use stream mode when updates should appear as soon as possible, and batch mode
when nothing may ever appear out of order and a short wait is fine. Choose the
timeout deliberately: it decides how long a customer sees an old status when a
message is lost.

## How to recognise this in code you did not write

- `.resequence(header("seq")).stream().timeout(...)`.
- `.resequence(...).batch().size(...)`.
- Sequence numbers in message headers.

## Where you have already met this

- Camel's `resequence()` and Spring Integration's resequencer.
- TCP, which reorders packets by sequence number before an application sees them.
- Kafka, which keeps order within a partition, so order keys are chosen for that.
