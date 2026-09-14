# Bulkhead — UML Sequence Diagrams

Four sequences over the same outage. Throughout, the partner API is slow — it answers
eventually, it just does not answer *now* — and a job waiting on it holds its thread.
Every line below comes out of `./gradlew run`.

## Act One: One Shared Pool Of Four

![Shared pool versus partitioned](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant F as SupplierFeed
    participant P as shared pool (4 threads)
    participant C as Checkout
    participant S as Shopper

    F->>P: importBatch(1..4)
    P->>P: shared-worker x4 all taken
    Note over P: every thread is waiting on the partner API

    S->>C: pay for ORD-5001
    C->>P: give me a thread
    P--xC: none free
    Note over C,P: still waiting after 300ms — the sale is lost

    Note over F,S: checkout has NO line in the timeline.<br/>It never started. It was never broken.
```

</details>

Four batches take four threads and hold them. Checkout asks for a thread and there is
not one.

The line to stare at is the note at the bottom. In the real timeline, checkout does
not appear *at all* — not as an error, not as a slow entry, not as anything. Absence
is the symptom, which is precisely why this is so hard to diagnose while it is
happening: there is nothing in the logs to read.

`theStarvedCheckoutWasNeverBroken` runs that same checkout job the instant a thread is
free and watches it succeed. **Starved and broken look identical from outside, and
only one of them can be fixed in the code.**

## Act Two: Two Bulkheads

```mermaid
sequenceDiagram
    autonumber
    participant F as SupplierFeed
    participant FB as feed bulkhead (2 threads, queue 2)
    participant CB as checkout bulkhead (2 threads)
    participant C as Checkout
    participant S as Shopper

    F->>FB: importBatch(1..4)
    FB->>FB: feed-worker x2 busy, 2 queued
    Note over FB: just as jammed as before — nothing was fixed

    S->>C: pay for ORD-5001
    C->>CB: give me a thread
    CB-->>C: checkout-worker, free
    C-->>S: paid ORD-5001

    Note over FB,CB: different threads. no demand on one<br/>can produce a thread on the other.
```

Same slow partner, same four batches, same instant. Checkout completes in
milliseconds.

The claim worth being careful about is not that checkout worked — it is that the feed
is *still stuck while it works*. `theFeedIsGenuinelyStuck` asserts exactly that,
because without it you cannot tell isolation from luck: a run where the partner
happened to recover would look the same. Nothing about the partner API was fixed.

`poolsDoNotBorrowFromEachOther` then pins the mechanism by name: work submitted to the
feed runs on `feed-worker`, work submitted to checkout runs on `checkout-worker`, and
neither pool will lend.

## Act Three: A Fifth Batch, With Nowhere To Go

```mermaid
sequenceDiagram
    autonumber
    participant F as SupplierFeed
    participant FB as feed bulkhead
    participant Q as ArrayBlockingQueue(2)

    F->>FB: importBatch(1), importBatch(2)
    FB->>FB: both running
    F->>Q: importBatch(3), importBatch(4)
    Q-->>FB: queued, waiting for a thread

    F->>FB: importBatch(5)
    FB--xF: BulkheadFullException — in 0ms

    Note over F,Q: 4 accepted, 1 refused
    Note over F: an unbounded queue would have taken it,<br/>and every batch after it, until memory ran out
```

Two threads busy, two jobs queued, and the queue holds two. The fifth batch is
refused, and `theRefusalIsFast` asserts it comes back immediately.

That speed is the whole value. The caller still has time to do something useful — shed
the batch, degrade, write it down for tonight. This is the circuit breaker's fast
failure applied to a queue rather than to a broken service.

An unbounded queue would have accepted batch five, and six, and every one after, and
told nobody anything. The failure does not go away; it is converted from a fast,
visible refusal into an out-of-memory error at an hour of its choosing.

## Act Four: The Bill, On A Quiet Afternoon

```mermaid
sequenceDiagram
    autonumber
    participant FB as feed bulkhead
    participant CB as checkout bulkhead

    Note over FB: 2 threads · 2 busy · 2 jobs queued and waiting
    Note over CB: 2 threads · 0 busy · 2 idle

    FB--xCB: cannot borrow
    CB--xFB: not allowed to help

    Note over FB,CB: one shared pool of four would have run<br/>all four batches at once, and finished sooner
```

Not really a sequence — an argument drawn as one, because the shape is the point.
Two threads are doing nothing beside two jobs that are waiting for a thread, and the
walls are what stop them helping.

`thesharedPoolIsFasterOnAGoodDay` asserts the other side of it: one pool of four runs
all four batches at once, four busy threads and an empty queue.

**Partitioned pools are idle capacity by design.** That is the price, it is paid every
day including the days nothing goes wrong, and it is worth paying for work whose
failure ends the business.

## Notes

- Nothing in these diagrams is simulated. This is the only project in the category
  with real threads, because the subject *is* threads genuinely waiting for one
  another — so there is no `SimulatedClock` here, and the timestamps in the demo are
  real milliseconds.
- The partner API's slowness is a `Gate`, a `CountDownLatch` the test opens when it
  chooses. A job waiting at a closed gate holds its thread exactly as a job waiting on
  a slow network does. Nothing sleeps, so the suite is fast and not flaky.
- Where a test has to prove something is *not* happening, it uses a short bounded
  `Future.get`: `oneSharedPoolStarvesCheckout` expects a `TimeoutException` after
  250ms, which is the shopper's patience rather than a guess about scheduling.
- In a real service these pools would be an executor per dependency, or a semaphore
  per downstream call, or separate connection pools. Every argument above is unchanged.
