# Determinism — How This Project's Failures Are Forced

Every test and every demo act in this project is deterministic. No test
under `src/test` contains a `Thread.sleep` used to wait for another
thread. `LOOKUP_MILLIS` is the demo's one named, measured subject;
`CooperativeCancellation`'s three short sleeps are the anti-pattern being
demonstrated, not a substitute for synchronization; and act five's rescue
timeout ends a genuine, otherwise-permanent hang rather than waiting for
anything to finish.

## The three harness pieces, reused unchanged from §46

**`Gate`**, **`Rendezvous`** and **`StepExecutor`** are copied verbatim
from `producer-consumer-pattern`, proven again in this project's own
`HarnessSelfTest` before anything else relies on them.

## How each specific scenario in this project is forced

**"All three lookups are genuinely in flight at once, not merely
submitted one after another"** (`ConcurrentProductPageTest`) — each of the
three lookups counts down a shared `CountDownLatch` the instant it starts,
then parks on its own `Gate`. The test waits on that latch before opening
any gate, so "all three are running concurrently" is a confirmed fact
before the test proceeds — not an inference from a short elapsed time.

**"The reader genuinely blocks until the writer completes the same
future"** (`FutureAndPromiseTest`) — the writer's own work is parked
behind a `Gate` that a second thread opens; `writerRan` can only become
true after that gate opens, so asserting it is true after `handOff`
returns proves the writer's work ran to completion before the reader's
`get()` could possibly have returned — the ordering is structural, not
timed.

**"A task waiting forever always times out, never returns"**
(`UnboundedWaitTest`) — the submitted task parks on a `Gate` this test
never opens. There is nothing to force: a gate that is never opened stays
closed on every run, so `get(timeout, unit)` reaching its timeout is not
a probability, it is the only possible outcome.

**"Cancelling a running task does not stop a task that ignores
interruption"** (`CooperativeCancellationTest`) — a `CountDownLatch`
confirms the task has actually started, and is inside its loop of ignored
`InterruptedException`s, before `cancel(true)` is called. Calling cancel
before the task starts would let the executor skip running it entirely,
which would prove nothing about a *running* task ignoring interruption —
this was an actual bug caught during this project's own development,
fixed by adding the latch.

**"An exception thrown inside a task surfaces later, wrapped, with a
stack trace containing none of the calling thread's frames"**
(`AsyncFailureTest`) — no forcing needed. A single-thread executor runs
the doomed task on a worker thread whose call stack the calling thread's
frames were never part of in the first place; the assertion checks a
structural fact about how `Throwable` captures its stack trace, not a
timing-dependent one.

## What the scheduler really does

Every technique above pins one specific fact — a lookup has started, a
gate will never open, a task has begun its loop — so a lesson can be
shown on every run. The real JVM scheduler chooses freely everywhere this
project does not pin something directly: which of three submitted
lookups a pool's workers pick up first, exactly how many milliseconds a
real 200ms sleep actually takes on a loaded machine, and more. A passing
test here proves the forced scenario behaves as shown — not that Future
and Promise are safe under every possible schedule a busier machine might
produce.
