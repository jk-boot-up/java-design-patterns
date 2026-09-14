# Bulkhead, Explained

## In One Sentence

Stop letting every kind of work draw from the same pot of threads: give the work that
must never be starved a pot of its own, so that a slow job filling up its own pot
cannot take the last thread the important work needed.

## Everyday Analogy: The Ship's Hull

A bulkhead is not a metaphor borrowed from somewhere else. It is the actual word for
the walls that divide a ship's hull into watertight compartments.

Punch a hole below the waterline in an undivided hull and the water spreads the length
of the ship. Punch the same hole in a divided one and one compartment floods. The ship
sits lower and it keeps going.

Two things are worth taking from that, and the second is the one people skip.

**First: nothing about the hole changed.** The bulkhead did not make the hull
stronger, or the sea calmer, or the damage smaller. Exactly as much water came in. All
that changed is how far it could spread.

**Second: look at where the walls are.** They take up space. A compartment can be
sitting completely empty while the one next door is packed, and you cannot move the
space between them. That is not a flaw in the design — it *is* the design. Isolation
is paid for in capacity you are not allowed to use.

## The Mechanism Is Almost Nothing

Here is the whole of it, and it is worth being disappointed by:

```java
new ThreadPoolExecutor(threads, threads, 0L, MILLISECONDS,
        new ArrayBlockingQueue<>(queueCapacity),
        runnable -> new Thread(runnable, name + "-worker"));
```

A fixed pool, a bounded queue, and a name. There is no algorithm here, nothing
adaptive, nothing to tune at runtime.

Say that out loud, because it is the point: **a bulkhead is not a clever piece of
machinery, it is a decision to stop sharing.** The pattern lives in having *two* of
them, not in anything either one does.

Which means the interesting work is not writing the class. It is deciding where the
walls go.

## Act One: The Shared Pool

One pool of four threads, and a partner API that has gone slow:

```
  ~  10ms  shared     feed-4         started on shared-worker
  ~  10ms  shared     feed-3         started on shared-worker
  ~  10ms  shared     feed-2         started on shared-worker
  ~  10ms  shared     feed-1         started on shared-worker
  checkout: still waiting for a thread after 300ms
```

Four batches, four threads, and they are all called `shared-worker`. Checkout has no
line in that timeline at all, because it never started.

`theStarvedCheckoutWasNeverBroken` then takes that same checkout job and runs it the
moment a thread is free, and it completes perfectly. There is nothing wrong with it.
It was starved, not broken — and the two look identical from the outside, which is
exactly what makes this failure so hard to diagnose at three in the morning.

## Act Two: The Same Outage, Partitioned

Now two bulkheads. The feed gets two threads; checkout gets two threads:

```
  ~   0ms  feed       feed-1         started on feed-worker
  ~   0ms  feed       feed-2         started on feed-worker
  ~   0ms  checkout   checkout       started on checkout-worker
  ~   0ms  checkout   checkout       finished
  checkout: paid ORD-5001
  the feed is jammed -- 2 threads busy, 2 jobs queued --
  and the shop is still selling, because it never shared.
```

Read the thread names, because they are the entire argument. `feed-worker` and
`checkout-worker`. Those are different threads, and no amount of demand on one side
can produce a thread on the other.

The important claim here is not that checkout worked — it is that the feed is *just as
stuck as before*. `theFeedIsGenuinelyStuck` asserts that while the sale goes through,
and it matters: without it you could not tell isolation from luck. Nothing was fixed
about the partner API. `checkoutKeepsWorkingIndefinitely` then puts a run of sales
through while the feed sits there, so it is not a one-off either.

## Act Three: A Full Bulkhead Refuses

Two threads and a queue of two hold four batches. A fifth arrives:

```
  feed is full: no thread and no room in the queue (in 0ms)
  4 accepted, 1 refused
```

The refusal is immediate, and `theRefusalIsFast` asserts that it is. This is the same
idea as the circuit breaker's fast failure, applied to a queue rather than to a broken
service: the caller finds out in a millisecond and still has time to do something —
shed the request, degrade, try later, write it somewhere for tonight.

An unbounded queue would have accepted that batch, and every batch after it, and
nobody would have found out anything until the process ran out of memory instead of
out of threads. **Refusing is a feature.** A queue that never says no is not generous,
it is a slow leak with good manners.

## Act Four: What It Costs

```
  feed:     2 threads, 2 busy, 2 queued and waiting
  checkout: 2 threads, 0 busy, 2 idle
```

Read those two lines together and let them be uncomfortable. Two threads are doing
nothing, while two jobs are waiting for a thread. They are not allowed to help.

One shared pool of four would have run all four batches at once and finished the
import sooner — and `thesharedPoolIsFasterOnAGoodDay` asserts precisely that, with the
shared pool showing four busy threads and an empty queue.

**Partitioned pools are idle capacity by design.** Not a bug, not a tuning problem.
That is what you are buying with, and any description of this pattern that does not
say so is describing something free, which this is not.

## So Where Do The Walls Go?

The trade is worth making for anything that must never be starved — the thing whose
failure ends the business, which in a shop is taking money.

It is not worth making for everything. A shop with fifteen bulkheads has fifteen pools
to size, fifteen numbers that drift out of date, and a lot of threads doing nothing at
three in the afternoon. The useful instinct is two or three partitions drawn along the
lines of *what must survive*, not along the lines of the package structure.

And the classification is a business decision, not a technical one. Nobody can tell
from the code that the supplier feed is less important than checkout. That fact lives
in the heads of the people who run the shop, and if it is not written down somewhere —
as a pool, as a number — then during the outage it is decided by whichever job
happened to ask for a thread first.

## What It Buys

- A slow dependency can no longer starve unrelated work of threads.
- The failure is contained *and named*: the feed's pool is full, which is a sentence
  an on-call engineer can act on, unlike "the site is slow".
- Callers of the saturated work find out immediately and can degrade.
- The blast radius is a decision you made in advance, in daylight, rather than an
  accident of scheduling during an incident.

## What It Costs

- **Idle threads beside waiting work**, permanently, by design.
- **Lower peak throughput** than one shared pool of the same total size.
- **More numbers to size**, and they drift as traffic changes.
- **A judgement call per partition** about what must never be starved — which no
  library can make for you, and which nobody remembers to revisit.

## When Not To Use It

When there is only one kind of work. Partitioning a service that does exactly one
thing gives you a smaller pool and no isolation, because there is nothing to isolate
it from.

When the work is genuinely uniform in importance and latency, dividing it just lowers
your throughput and gives you two numbers to get wrong instead of one.

And when the real problem is that a dependency is broken, a bulkhead alone is a
bandage. It stops the damage spreading; it does not stop you calling the dead thing.
That is the circuit breaker's job, and the two belong together: a breaker so you stop
calling a service that has stopped answering, and a bulkhead so that the calls still
in flight cannot drown anything that matters.

## What To Remember

1. A bulkhead is a decision to stop sharing, not an algorithm.
2. Starved and broken look identical from outside, and only one of them is fixable in
   the code.
3. A bigger shared pool does not fix this. It moves the number and hides the failure
   for longer.
4. Prove the slow job is still stuck, or you have not shown isolation — you have shown
   a coincidence.
5. Bound the queue. A queue that never refuses converts a fast failure into an
   out-of-memory one.
6. Refusing immediately is a feature: it leaves the caller time to do something else.
7. Isolation is paid for in idle threads, and you must be able to say that out loud.
8. Draw the walls along what must survive, not along the package structure.
9. Two or three partitions, not fifteen.
10. Pair it with a circuit breaker. They solve the same outage from opposite ends.
