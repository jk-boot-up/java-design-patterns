# Determinism — How This Project's Failures Are Forced

Every test and every demo act in this project is deterministic. No test
under `src/test` contains a `Thread.sleep`. The demo's one named delay,
`PACK_MILLIS`, is the same subject §46 measures; act five's timeout is a
rescue from a genuine deadlock, not a wait for anything to finish.

## The three harness pieces, reused unchanged from §46

**`Gate`**, **`Rendezvous`** and **`StepExecutor`** are copied verbatim
from `producer-consumer-pattern`, proven again in this project's own
`HarnessSelfTest` before anything else relies on them. See §46's own
`determinism.md` for the full account of each; this document covers only
what is specific to a pool of more than one worker.

## How each specific scenario in this project is forced

**"Both workers are busy, and 500 more orders still queue instead of
blocking or rejecting"** (`UnboundedPoolPackingTest`, and demo act two) —
both of the pool's two workers are handed a task that counts down a
`CountDownLatch` the instant it starts, then parks on a `Gate`. The test
waits on that latch before submitting a single real order, so "both
workers are busy" is a confirmed fact, not a hope, before `backlog()` is
read.

**"The queue reaches its stated capacity, and the next submission is
rejected on the spot"** (`BoundedPackingPoolTest`, and demo act three) —
the same held-first-task technique, this time with exactly one worker.
Once a `CountDownLatch` confirms that worker is parked on a `Gate`, three
real orders are submitted — filling the bounded queue exactly, since
nothing is taking from it — and a fourth is submitted while the worker is
still provably parked. Because `ThreadPoolExecutor.execute` runs its
rejection handler synchronously, the assertion needs no wait at all: the
call that submits the fourth order returns only after the handler has
already run.

**"A task waiting on a task in its own one-worker pool never resolves on
its own"** (`PoolStarvationTest`) — this scenario needs no forcing.
`Executors.newFixedThreadPool(1)` has exactly one worker; that worker is
the one running the outer task and waiting on the inner one; the inner
task can never be scheduled, on any scheduler, because there is only ever
one worker to schedule it onto. The `timeoutMillis` argument to
`PoolStarvation.attemptNestedSubmit` is not synchronization — it is the
only thing that ends the test, and the assertion that `waitedMillis` is
at least that long is itself part of the proof: nothing shorter is
possible, because nothing resolves the wait early.

**"A pool with a free second worker does not starve on the same nesting"**
(`PoolStarvationTest.aPoolWithTwoWorkersDoesNotStarveOnOneNestedSubmit`)
— the positive control. With two workers, the inner task always finds
one free, and `attemptNestedSubmit` returns well before its timeout —
proving the starvation above is a property of the pool having exactly one
worker, not of nesting a submit call in general.

## What the scheduler really does

Every technique above pins one specific interleaving so a lesson can be
shown on every run, exactly as §46 explains at length. This project adds
one exception worth naming directly: the pool starvation deadlock needs
no interleaving forced onto it at all. A single-worker pool waiting on
itself has exactly one possible outcome regardless of what the scheduler
does with anything else — the only "race" in that scenario is how long
the demonstration is willing to wait before giving up on it.
