# Determinism — How This Project's Failures Are Forced

Every test and every demo act in this project is deterministic. No test
under `src/test` contains a `Thread.sleep`, and the one delay anywhere in
the demo — how long packing takes — is named as the subject being measured,
not hidden as a wait.

## The three harness pieces, and where each is used

**`Gate`** — a one-shot door a thread parks at until the test opens it.
Used everywhere a thread needs to be provably *not finished yet*:
`InlineCheckoutTest` proves checkout has not returned by holding packing
closed; `ThreadPerOrderCheckoutTest` proves three checkouts produced three
live threads the same way; every act in the demo that needs a thread parked
mid-work uses one.

**`Rendezvous`** — an n-party barrier that forces two or more threads to be
at the same instant before either proceeds. `HarnessSelfTest.rendezvousForcesTheLostUpdateEveryRun`
is the proof: two threads each read a shared value, meet at the rendezvous,
then both write back a value derived from what they read. Without the
rendezvous this is "wrong sometimes". With it, it is wrong on all twenty
repetitions.

**`StepExecutor`** — a queue with a manual crank. Nothing runs until
`runNext()` is called, on whichever thread calls it. Proven in
`HarnessSelfTest.stepExecutorRunsNothingUntilStepped`. This project does not
lean on it directly — Thread Pool and Active Object, later in the category,
do — but it is proven here, in the reference project, before it is reused.

## How each specific scenario in this project is forced

**"Checkout does not return until packing finishes"**
(`InlineCheckoutTest`) — packing is a `Gate`. The test starts a checkout on
its own thread, confirms with a bounded `join(100)` that the thread has not
died (it cannot have — the gate has not been opened), then opens the gate
and confirms the checkout completes.

**"The queue really is full, and a fourth order is rejected"**
(demo act three, and the same shape in `BoundedOrderQueueTest`) — the
packer's *first* pack call is a `Gate`, held closed. A `CountDownLatch`
counts down the instant the packer has taken that first order and is
parked mid-pack, so the test knows, with certainty rather than a guess,
that the packer cannot race the next three `put` calls for a queue slot.
Only once that latch has fired are the remaining orders enqueued, and only
then is "the queue is at capacity" a fact rather than a hope.

**"A poison pill drains everything queued before it"**
(`PackerTest.poisonDrainsEverythingQueuedBeforeIt`) — no timing at all. The
pill is enqueued after four real orders, on a `BlockingQueue`, whose
ordering guarantee does the rest.

**"Interrupting the packer loses whatever is still queued"**
(`PackerTest.interruptingThePackerLosesWhateverIsStillQueued`, and demo act
five) — the same held-first-order technique as the queue-full scenario,
followed by `Thread.interrupt()` on the packer thread rather than a poison
pill. `Packer` checks `Thread.currentThread().isInterrupted()` after every
`pack` call, and only logs an order as packed if that flag is still clear —
which is what stops the held order itself from being wrongly recorded as
packed when the interrupt lands.

## What the scheduler really does

Every technique above pins one specific interleaving so a lesson can be
shown on every run. **The real JVM scheduler chooses none of this freely
elsewhere.** Outside a test, two checkout threads might interleave in any
order the operating system's scheduler decides, on any given run, on any
given machine — the failures this project demonstrates are bugs on *some*
schedules, not a schedule this project has discovered is the only one that
exists. A reader who believes a passing test proves a concurrent design is
safe on every possible schedule has been taught something false. What a
passing test here actually proves is narrower and still valuable: that the
one interleaving forced onto the naive version produces the failure it is
supposed to, and that the pattern version, under the same forced
interleaving, does not.
