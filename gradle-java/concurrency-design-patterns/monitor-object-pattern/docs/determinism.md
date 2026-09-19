# Determinism — How This Project's Failures Are Forced

No test under `src/test` calls `Thread.sleep`. The three harness pieces,
`Gate`, `Rendezvous` and `StepExecutor`, are copied unchanged from
Producer–Consumer and proven again in `HarnessSelfTest`.

**The lost update** (`PlainStockTest`, `VolatileStockTest`) — the stock
takes a hook that runs between the read and the write. The test passes a
two-party `Rendezvous` as the hook, so both threads have read ten before
either writes nine. The answer is nine on every run.

**The forgetful caller** (`CallerLockedStockTest`) — one thread takes the
lock; the other does not. Both meet at the rendezvous holding the same
stale read. The lock the careful thread holds does not stop the other.

**`if` instead of `while`** (`IfInsteadOfWhileTest`) — the demo polls the
condition's own wait-queue length until both takers are waiting, then adds
one item and wakes both. Both skip the check and the count is minus one.

**A second caller is blocked** (`StockMonitorTest`) — one thread parks
inside the monitor at a gate. A second thread's thread state is polled
until it reads `WAITING`, which proves it is parked on the lock.

**Nested monitors** (`MonitorHazardsTest`) — a rendezvous makes both
threads hold their first monitor before either asks for the second.
`ThreadMXBean.findDeadlockedThreads()` then reports the deadlock, and
interrupting both threads breaks it.

**Calling out while holding the lock** — needs no forcing. The reading
thread can never get the lock, so the timeout is the only outcome.

## What the scheduler really does

The harness pins one fact per scenario and leaves the rest to the JVM.
Act four's timing is a real measurement and varies. The lesson is the
shape of the results, not the milliseconds.
