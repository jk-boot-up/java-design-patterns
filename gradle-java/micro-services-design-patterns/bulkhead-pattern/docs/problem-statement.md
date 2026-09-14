# Problem Statement

## The Scenario

The shop runs on one application with one thread pool. Every piece of work it does —
serving a product page, taking a payment, sending a confirmation email, importing the
nightly supplier catalogue — asks that pool for a thread, does its job, and gives the
thread back.

That is a completely ordinary way to build a service, and for a long time it is the
right one. Threads are expensive, a pool is the standard way to bound how many exist,
and having a single pool means there is a single number to tune.

Two jobs in that shop matter here.

**Checkout** takes a shopper's money. It is fast, it is correct, and nobody has ever
filed a bug against it. It needs exactly one thing: a thread.

**The supplier feed** imports the supplier's catalogue overnight. Nobody is waiting
for it. If it finished an hour late nothing bad would happen. It calls a partner API
which is, occasionally, very slow.

## What Goes Wrong

One night the partner API stops answering promptly. Not failing — answering, but
slowly. Each import batch makes its call and waits.

A job that is waiting holds its thread. It is not using the CPU, it is not doing
anything at all, but the thread belongs to it until the call comes back. Four batches
start, four threads are taken, and the pool has four threads.

```
  ~  10ms  shared     feed-4         started on shared-worker
  ~  10ms  shared     feed-3         started on shared-worker
  ~  10ms  shared     feed-2         started on shared-worker
  ~  10ms  shared     feed-1         started on shared-worker
  checkout: still waiting for a thread after 300ms
```

Read what is *missing* from that timeline rather than what is in it. Checkout has no
line. It never started.

## Why That Hurts

It would be easier to accept if checkout were broken. It is not. A test in this
project — `theStarvedCheckoutWasNeverBroken` — takes exactly the same checkout job,
runs it the moment a thread is free, and watches it complete correctly. There is
nothing to fix in it.

It simply could not get a thread, and by the time one came free the shopper had gone.

So the sentence that matters is this one: **the shop stopped selling because of a
background job that nobody was waiting for.** Not because the background job was
wrong, not because checkout was wrong, but because the two of them were drawing from
the same pot.

And notice how invisible that coupling is. Nothing in the code of either job mentions
the other. There is no import, no call, no shared variable. They are connected only
by a resource neither of them names.

## The Tempting Fix, And Why It Is Not One

The obvious response is: make the pool bigger. Four threads was too few, so use forty.

That buys time and nothing else. The feed's batches will take forty threads instead
of four whenever the partner API is slow enough for long enough, and checkout will be
starved at forty exactly as it was at four. The number changes; the failure does not.
Worse, the bigger the pool the longer it takes for anyone to notice, and the more
memory the eventual pile-up consumes.

The second tempting fix is an unbounded queue — never refuse a job, just let them
wait. That sounds generous. What it actually does is convert a fast, visible failure
into a slow, invisible one: jobs accumulate until the process runs out of memory, and
every caller waits for work that will not start for minutes.

## The Question This Project Answers

If the two jobs are connected only by the pool they share, what happens if they stop
sharing it?

## The Second Half, Which Is Harder

Partitioning is not free, and any treatment of this pattern that only shows the good
day is selling something. Give the feed two threads and checkout two threads, and on
a quiet afternoon you get this:

```
  feed:     2 threads, 2 busy, 2 queued and waiting
  checkout: 2 threads, 0 busy, 2 idle
```

Two threads doing nothing, beside two jobs that are waiting for a thread. One shared
pool of four would have run all four batches at once and finished the import sooner.

So the honest question is not "should I use bulkheads" but "which work must never be
starved, and what am I willing to leave idle to guarantee it?" That is a decision
about the business, made in advance, and it is the part no library can make for you.

## The Goal

1. Show a shared pool starving a job that is not broken, and prove it is not broken.
2. Show the same outage with the work partitioned, and prove the slow job is *just as
   stuck* — so the isolation is demonstrably the reason, not luck.
3. Show what a full bulkhead does, and why it refuses rather than queues forever.
4. Show the cost, in idle threads, without flinching.
5. Do all of it with real threads and no sleeping, so the tests are fast and not flaky.
