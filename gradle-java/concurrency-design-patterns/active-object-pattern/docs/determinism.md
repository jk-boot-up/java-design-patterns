# Determinism — How This Project's Failures Are Forced

No test under `src/test` calls `Thread.sleep`. `Gate`, `Rendezvous` and
`StepExecutor` are copied unchanged from Producer–Consumer and proven
again in `HarnessSelfTest`.

**A caller blocked behind a slow import** (`MonitorInventoryTest`) — the
import parks on a gate while holding the lock. A `CountDownLatch` confirms
it is inside. The checkout thread's state is then polled until it reads
`WAITING`.

**A call that returns first** (`InventoryActiveObjectTest`) — the same
shape. The worker is parked on a gate, confirmed by a latch, and only then
is `reserve` called. `isDone()` must be false. Opening the gate lets the
futures complete in order.

**No lost updates without a lock** — four threads restock at once, released
together by a gate. The total must be exact. There is no lock to credit;
the single worker is what makes it hold.

**The mailbox backing up** (`MailboxTest`) — the worker is parked, more
messages are sent, and the mailbox size is read before the gate opens.

**An error from the worker** — the exception is created inside the
message, on the worker, so its stack trace holds the worker's frames only.

**The throughput ceiling** — every message spins for 50 microseconds of
real work. One caller and four callers finish in about the same time. The
test asserts only that four callers do not double the rate.

## What the scheduler really does

The harness pins the state each scenario needs. Rates are real
measurements and vary by machine.
