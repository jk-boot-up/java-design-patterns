# Producer–Consumer, Explained

## The pattern in one sentence

A bounded queue sits between whoever produces work and whoever consumes
it, so each side runs at its own pace up to a limit that is chosen on
purpose, not discovered by accident.

## Why "bounded" is the whole pattern

An unbounded queue is not a safer version of this pattern — it is the
second naive version from the problem statement, wearing a nicer name.
`ThreadPerOrderCheckout` never runs out of threads to create until the
machine does; a checkout backed by an unbounded queue never runs out of
queue slots until the machine does, for the same underlying reason: nothing
anywhere says no. `BoundedOrderQueue` wraps a plain `ArrayBlockingQueue`
with a fixed capacity precisely so that "no" is a decision this project
gets to make on purpose, rather than a decision the operating system makes
for it, later, at the worst time.

## The two ways "no" can be said

**Block the producer.** `BoundedOrderQueue.put` waits until there is room.
Checkout gets slow again — which is the same cost the first naive version
paid, now only when the queue is genuinely full rather than on every
order.

**Reject the order.** `BoundedOrderQueue.offer(order, timeout, unit)`
waits up to a patience window and then gives up. Demonstrated directly in
this project's act three: a queue at capacity, held there deterministically
by a packer parked mid-pack, correctly rejects a fourth order after its
150ms patience runs out.

There is no third, pleasant option. Grow without limit is the failure this
pattern exists to fix, not an option it offers.

## Two shutdowns, and they are not the same event

**Clean.** `Packer.POISON` is enqueued like any other order. Because it
travels through the same `BlockingQueue`, everything queued ahead of it is
still taken and packed, in order, before the packer sees the pill and
stops. Four orders queued, then the pill: all four get packed.

**Abrupt.** `Thread.interrupt()` on the packer thread stops it wherever it
currently is — mid-`take()`, or mid-`pack()` if the packing step itself
notices the interrupt. Whatever was still in the queue behind it is never
reached. One order held mid-pack, four more queued behind it, then an
interrupt: zero of the four are ever packed, and they are still sitting in
the queue afterward, demonstrably.

Confusing these two is a real, common bug: shutting a service down with a
raw `interrupt()` when a `poison` pill — or an equivalent orderly-stop
signal — was what was actually wanted, quietly drops whatever work was
queued at the moment someone pulled the plug.

## What the scheduler really does

See [`determinism.md`](determinism.md) for the full account. In short:
every deterministic outcome above is bought by pinning one specific
interleaving with a `Gate` or a `CountDownLatch`. The real JVM scheduler
is free to run producer and consumer threads in whatever order it likes,
on whatever machine is running them, and the fact that this project's
tests pass on every run proves that the *forced* interleaving produces the
stated outcome — not that every possible interleaving does.

## The bill

**Ordering is not guaranteed by the queue alone**, beyond FIFO for a
single producer and single consumer — add a second producer and two
orders that arrived in one sequence can be taken in either order, because
nothing about "bounded" says anything about fairness between producers.

**A full queue is back-pressure reaching all the way to checkout.** If the
policy is "block", a slow packer eventually makes checkout slow again —
the exact problem this pattern exists to fix, now one layer removed and
easier to miss, because it only shows up once the queue fills.

**Choosing the bound is a real decision with no free answer.** Too small
and ordinary bursts trigger rejections or blocking; too large and the
project has quietly rebuilt the unbounded queue, just with a very long
fuse.

## When this is too much

Worth it the moment producing and consuming genuinely happen at different,
independent rates — which is most real systems with any I/O in them at
all. Not worth it for two pieces of code that always run in lockstep
anyway; a queue between two things that can never get out of step with
each other is ceremony with no back-pressure decision behind it.
