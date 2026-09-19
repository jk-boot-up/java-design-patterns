# Problem Statement

## The scenario

Checkout accepts orders. A packing step — wrapping and labelling the order
for the courier — handles each one, and packing is slower than orders
arrive. That gap between arrival speed and processing speed is this
project's entire subject.

## The naive version, in two parts

### Part one: the checkout thread packs the order itself

`InlineCheckout` does exactly this: `checkout()` calls `pack()` directly,
and does not return until packing finishes. It is correct, and the cost is
paid by the shopper directly — every checkout call blocks for as long as
packing takes, and one slow pack blocks every checkout behind it, because
there is only one thread and it can only do one thing at a time.

```
ONE. No queue at all — checkout packs the order itself.
  checkout(ord-1) returned after 49ms
  checkout(ord-2) returned after 50ms
  checkout(ord-3) returned after 50ms
```

### Part two: a thread per order

The fix most people reach for first: hand each order to a brand new
thread and return immediately. `ThreadPerOrderCheckout` does this, and it
works — the shopper is never held up. The cost shows up later, and it is
not hypothetical: thread creation has a real, measurable cost, each thread
holds a stack whether or not it is doing anything, and if arrivals ever
outpace packing there is nothing anywhere applying a brake. Extrapolated
from a real, safely capped measurement:

```
TWO. A thread per order — works, until it does not.
  created 2,000 real threads in 96.8ms (48.4 microseconds each)
  at that rate, 100,000 threads costs roughly 4838ms of creation alone —
  before any of them has packed a single order.
```

Every thread that outlives its usefulness while waiting on a slow pack is a
stack that has to live somewhere, and the failure everyone eventually meets
is `OutOfMemoryError: unable to create native thread`. This project does
not trigger it — a demo that can wedge the machine running it is not a
teaching aid — but the curve above is real, measured, and points straight
at the cliff.

## What the pattern must deliver

A **bounded** queue between checkout and packing. Producers offer orders,
the packer takes them, and each runs at its own pace — up to the bound.
The bound is not an implementation detail; it is the entire point, and this
project has to show the queue actually full and show what a producer does
when there is nowhere left to put the work: block, or be rejected. It also
has to show both ways a running system stops — a clean shutdown that drains
whatever is already queued, and an abrupt one that loses it.
