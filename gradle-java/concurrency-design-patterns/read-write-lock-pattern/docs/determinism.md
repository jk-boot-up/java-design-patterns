# Determinism — How This Project's Failures Are Forced

Every test and every demo act in this project is deterministic. No test
under `src/test` contains a `Thread.sleep` anywhere, for any reason — this
is the first project in the category where even a named delay was not
needed, because the "work" being measured in acts two, three and six is
real, unpadded reads, not a simulated wait.

## The three harness pieces, reused unchanged from §46

**`Gate`**, **`Rendezvous`** and **`StepExecutor`** are copied verbatim
from `producer-consumer-pattern`, proven again in this project's own
`HarnessSelfTest` before anything else relies on them.

## How each specific scenario in this project is forced

**"A read lands in the gap between the two field writes, and sees a
price that was never true"** (`UnsynchronizedCatalogueTest`, and demo act
one) — the writer's own `midWrite` hook counts down a `CountDownLatch`
right after setting the new amount, then parks on a `Gate`. The test
waits on that latch before reading, so the read is proven to land after
the amount changed and before the currency did — not hoped to, by luck of
scheduling.

**"Several readers hold the read lock at the exact same moment"**
(`ReadWriteCatalogueTest`) — four reader threads each acquire the read
lock and then park on a shared `Gate`; a `CountDownLatch` confirms all
four are holding it before the test asserts
`ReentrantReadWriteLock.getReadLockCount()` equals four. The assertion
checks a fact the lock itself reports, confirmed true at a moment the
test controls, not inferred from timing.

**"A queued writer is barged by a fresh reader's `tryLock()`"**
(`WriterBargingTest`) — `ReentrantReadWriteLock.hasQueuedThreads()` is
polled in a spin-wait with no deadline until it reports true, which
proves the writer thread is genuinely parked in the lock's own AQS queue
before the barge is even attempted. The barge itself needs no forcing:
`tryLock()`'s behaviour here is documented in the JDK, not a race.

**"Upgrading a read lock to a write lock always deadlocks"**
(`UpgradeDeadlockTest`) — this scenario needs no forcing at all. A thread
already holding the read lock can never be granted the write lock while
any read lock — including its own — is held, on any scheduler, every
time. The `timeoutMillis` argument is not synchronization; it is the only
thing that ends the test, and the assertion that the elapsed wait is at
least that long is itself part of the proof.

**"Neither `SingleLockCatalogue` nor `SnapshotCatalogue` ever produces a
torn read, under real concurrent writes"**
(`SingleLockCatalogueTest`, `SnapshotCatalogueTest`) — a reader thread
spins continuously, checking every value it reads against the two prices
actually in use, while the main thread performs five thousand real
writes. Any value that matches neither price is a torn read; the
assertion is a simple boolean that stays false because the lock, or the
atomic reference, structurally prevents a torn read from ever being
constructible in the first place — not because five thousand writes
happened to avoid one.

## What the scheduler really does

Most of what this project measures does not need forcing, because the
scenario is either a documented API contract (`tryLock()`'s barging, the
upgrade deadlock) or a structural guarantee (an `AtomicReference` cannot
publish half a value). The throughput numbers in acts two, three and six
are the exception: they are real, unforced measurements of how eight
genuine reader threads actually interleaved on one real machine, and the
scheduler chose every detail of that. A different machine, under
different load, will report different milliseconds — the shape the
numbers take relative to each other is the lesson, not the exact figures.
