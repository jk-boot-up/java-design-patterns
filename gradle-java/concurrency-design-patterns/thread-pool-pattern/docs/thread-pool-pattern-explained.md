# Thread Pool, Explained

## The pattern in one sentence

A fixed, small number of worker threads is created once and reused for
every task handed to it, pulling from a queue whose own capacity is
chosen on purpose — the same "bounded, deliberately" idea §46 taught for
a queue, now applied to the workers pulling from it as well.

## Why "fixed" is not the whole pattern

`Executors.newFixedThreadPool(2)` really does cap the worker count at
two. It is still the naive version in this project, because the queue it
builds internally is unbounded. A pool with a bounded worker count and an
unbounded queue has moved the exact failure Producer–Consumer's naive
thread-per-order version has — nothing anywhere says no — from "too many
threads" to "too many queued tasks", and a queue that never says no is
`ThreadPerOrderPacking` wearing a nicer name. `BoundedPackingPool` bounds
both: a `ThreadPoolExecutor` built directly, with an `ArrayBlockingQueue`
of a fixed capacity in place of the unbounded queue the factory method
hides.

## Rejection here has no patience window

Producer–Consumer's `BoundedOrderQueue.offer(order, timeout, unit)` waits
up to a chosen window before giving up. `ThreadPoolExecutor.execute` has
no such window built in: the instant every worker is busy and the queue
is full, its rejection handler runs — synchronously, on the calling
thread, before `execute` returns. There is no waiting, no retry, nothing
free. `BoundedPackingPool`'s rejection handler simply counts what it
refuses; a real service might retry, shed load elsewhere, or apply its
own patience window on top — but that is code the caller has to write,
not something the pool gives away.

```
THREE. The pattern — a bound on workers, and a bound on the queue.
  1 worker busy, queue filled to capacity 3: 3
  one more order, submitted with the worker busy and the queue full: REJECTED on the spot — no patience window, no room
```

## The deadlock that exists at any pool size

A task running inside a fixed pool can submit a second task to that same
pool and wait for its result. If every worker is already busy — including,
as here, when the pool has exactly one worker and that worker is the one
waiting — the second task can never be handed a worker. It is queued
forever. This is not a slow path; left alone it never resolves, at any
queue capacity, because the queue was never the bottleneck — the worker
count was.

```
FIVE. Pool starvation — a task waiting on a task in its own pool.
  a fixed pool of 1: the running task submits a second task to that
  same pool and waits for its result — no free worker will ever run it.
  starved: true, rescued after 210ms by a demonstration timeout; left alone, this never resolves.
```

`PoolStarvation.attemptNestedSubmit` rescues the demo — and the test —
from actually hanging with a timeout, but that timeout is not the pool's
patience; it is the demonstration's own escape hatch. A real service that
does this hangs until an operator notices threads that are all "RUNNABLE"
and doing nothing, which is a far uglier debugging session than a test
failure.

## What the scheduler really does

See [`determinism.md`](determinism.md) for the full account, unchanged
from §46: every number above is bought by pinning one specific
interleaving with a `Gate` or a `CountDownLatch`. The real scheduler
chooses freely which worker picks up which queued task and in what order,
and the fact that this project's tests pass on every run proves the
*forced* interleaving produces the stated outcome — not that every
possible one does. The starvation deadlock is the one exception worth
naming directly: it needs no forcing at all, because a pool of one worker
waiting on itself has exactly one possible outcome, on every scheduler,
every time.

## Java's answer, stated plainly

Java 21's virtual threads change the arithmetic in act one dramatically —
this project measures the same 2,000-thread flood twice, once with
platform threads and once with virtual ones, and the difference is not
subtle:

```
SIX. Java's answer — virtual threads change the creation cost, not the bound.
  created 2,000 virtual threads in 11.4ms (5.68 microseconds each)
  compare act one: same count, real platform threads, measured the same way.
```

What virtual threads do not change is the reason a pool exists in this
project: bounding a *resource*, not a thread count. A downstream database
with ten connections available still has ten, whether a million virtual
threads or three platform threads are asking for one. Cheap thread-per-task
is a genuinely good answer for I/O-bound work that used to justify pooling
threads purely to avoid their creation cost — it is not an answer to "how
many things may run against this limited resource at once."

## The bill

**Sizing the pool is a real decision with no free answer**, in both
directions. Too few workers, and the queue in act two grew by five
hundred before anyone thought to ask why — a backlog that is invisible
until it is a heap dump. Too many workers, and each one is a stack held
open whether or not there is work for it, the same cost act one measures,
merely capped rather than removed.

**A pool with tasks that wait on other tasks in the same pool is a
deadlock waiting for the wrong day**, not a rare event — it happens on
every schedule, at every pool size, the moment nesting occurs. The fix is
architectural: never submit work to the same pool you are already running
inside of and then block waiting for it, at any size.

## When this is too much

Worth it the moment more than one worker genuinely helps — CPU-bound work
that can run in parallel, or I/O-bound work under java's traditional
platform-thread model where creation cost matters. Not worth it for a
single background task that runs once; a pool sized for concurrency it
will never use is ceremony with nothing to bound.
