# Future/Promise, Explained

## The pattern in one sentence

Each unit of work is submitted and immediately returns a handle to a
result that does not exist yet, so independent work can run at once
instead of one call waiting out the last before it even starts.

## Two halves, one object

A beginner hears "Future" and "Promise" used almost interchangeably, and
the confusion is reasonable: `java.util.concurrent.CompletableFuture` is
both at once, which is exactly why `FutureAndPromise.handOff` in this
project keeps them on two different threads on purpose.

**The Future is the reader's half.** Whoever holds it calls `get()` and
blocks until a value shows up. **The Promise is the writer's half.**
Whoever holds it calls `complete(value)` once its own work is done — and
nothing about that writer needs to know who is reading, or how many
readers there are.

```
THREE. Future and Promise — the two halves, made explicit.
  the writer thread completed the promise: £129.99
  the reader thread was blocked on the future until it did.
```

One piece of code completes exactly what another piece is waiting on, and
the object standing between them is the only thing either side needs to
agree on.

## The bill, paid honestly

**Exceptions move.** A task that throws does not throw where it was
called — it throws on whatever worker thread happened to run it, and the
failure only surfaces later, wrapped in an `ExecutionException`, when
something calls `get()`. The stack trace attached to that wrapped
exception belongs entirely to the worker thread; the frame for the code
that submitted the doomed task is not, and cannot be, part of it.

```
FOUR. Exceptions move — surfacing wrapped, on get().
  cause: catalogue unavailable for ESP-001
  stack top: com.jk.explore.futurepromise.ProductPageDemo.lambda$actFour$4(ProductPageDemo.java:107)
  the call site that submitted this task appears nowhere above: true
```

**`get()` with no timeout is a hang, not a wait.** A task that never
completes — this project parks one forever on a closed `Gate` — leaves a
bare `future.get()` blocked for as long as the caller is willing to sit
there, which by default is forever. `get(timeout, unit)` is not a nicety;
it is the only thing standing between "waiting" and "hung".

```
FIVE. get() with no timeout is a hang.
  a task parked forever, waited on with a 200ms rescue timeout:
  timed out: true, after 205ms
  a bare get() with no timeout does not time out — it just never returns.
```

**Cancellation is cooperative, and may do nothing.**
`Future.cancel(true)` interrupts the thread running the task — it does
not stop the task. A task that catches `InterruptedException` and carries
on, the way this project's own demonstration task deliberately does, keeps
running to completion regardless of `cancel` ever having been called.

```
SIX. Cancellation is cooperative, and may do nothing.
  cancel(true) reported: true
  the task ran to completion anyway: true
  it caught every interrupt and carried on — cancel asked; the task said no.
```

**Chained callbacks can reach a depth that is unreadable.** Nesting
`thenApply`, `thenCompose` and `thenCombine` calls to assemble one final
result from several futures is exactly as powerful as it looks in a small
example, and exactly as illegible once four or five steps are chained —
each level adds another closure, another indentation, and another place
an exception can be swallowed silently if `exceptionally` is forgotten at
that one level. `CompletableFuture`'s callback API is real and useful; it
is also the single easiest way in this whole category to write code
nobody, including its author, can read back a month later.

## What the scheduler really does

Every deterministic outcome above is bought by pinning one specific fact
with a `Gate`, a `CountDownLatch`, or — for the unbounded wait and the
cooperative cancellation — a real, bounded, named delay standing in for
"this genuinely never finishes" or "this genuinely takes a moment". The
real JVM scheduler decides freely which worker thread runs which
submitted task, and in what order, everywhere this project does not pin
it directly. A passing test here proves the forced scenario behaves as
shown — not that every possible scheduling of concurrent futures does.

## When this is too much

Worth it the moment two or more units of work are genuinely independent
and each takes real, measurable time — exactly this project's three
catalogue lookups. Not worth it for two calls that are already fast, or
for two calls where the second genuinely needs the first's result: there
is nothing to overlap, and a `Future` around work that was never going to
run concurrently with anything is ceremony with no payoff behind it.
