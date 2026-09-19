# Read–Write Lock, Explained

## The pattern in one sentence

Many readers may hold the lock together; a writer excludes everyone,
readers and other writers alike — because two reads can never conflict
with each other, only a write can conflict with anything.

## Why "correct" is not the whole story

`SingleLockCatalogue` is correct: one `ReentrantLock` around every read
and every write means no torn read is possible, full stop. It is also
needlessly conservative — it treats two readers exactly like a reader and
a writer, forcing them to take turns for no reason the data demands.
`ReadWriteCatalogue` fixes exactly that one thing: readers proceed
together; only a writer, holding the write lock, ever excludes anyone.

## The bill this project's own numbers insist on

**A queued writer is not guaranteed to go next.** The read lock's
`tryLock()` is documented, in the JDK itself, to acquire immediately
whenever the write lock is free — "whether or not other threads are
currently waiting for the read lock." A writer already parked, waiting
its turn, can be barged past by a reader that arrived after it.

```
FOUR. The mechanism behind writer starvation.
  writer genuinely queued, waiting: true
  a second reader's tryLock() barged past it anyway: true
```

Do this continuously, under a steady stream of readers, and a writer can
wait far longer than its own work would ever justify — this is what
"writer starvation" means in practice: not that the writer never runs, but
that nothing bounds how long it might have to wait.

**Upgrading a read lock to a write lock deadlocks the thread holding
it.** `ReentrantReadWriteLock` allows downgrading — acquire the write
lock, then the read lock, then release the write lock — but never the
reverse. A thread holding the read lock that then calls
`writeLock().lock()` waits for every reader, including itself, to
release — which it can never do, because it is blocked before it gets
the chance.

```
FIVE. Upgrading a read lock to a write lock deadlocks.
  same thread, holding the read lock, requests the write lock:
  deadlocked: true, rescued after 203ms by a demonstration timeout
  left alone, this thread waits on itself forever.
```

**The lock advertised for readers can lose to a plain mutex, for a
critical section this cheap.** This is not a hypothetical — it is what
this project's own act three and act six measure, honestly, on real
hardware:

```
SIX. When the lock loses.
  single mutex:      11ms
  read-write lock:    144ms
  immutable snapshot: 11ms
```

`ReentrantReadWriteLock` tracks how many readers currently hold the lock
through shared, atomically-updated state — every reader's lock and unlock
call touches it. Under heavy concurrent read traffic, all of those
threads contend on that one piece of shared memory continuously, even
though none of them is ever made to wait for another reader. A plain
`ReentrantLock`, letting exactly one thread through at a time, pays none
of that coordination cost — the threads not currently holding it are
simply parked, not competing. For a critical section as cheap as
returning a record reference, that coordination overhead is the larger
cost, not the smaller one.

## The honest conclusion

For this catalogue's size, an immutable snapshot swapped through an
`AtomicReference` beats both locks outright — no lock at all, because a
reader either sees the whole old price or the whole new one, never a
mixture, and there is no shared counter for concurrent readers to
contend on. `SnapshotCatalogue` is that idea in eleven lines.

## What the scheduler really does

Every deterministic outcome above that needs forcing is forced with a
`Gate` or a `CountDownLatch` — the torn read, the barged writer, the
several-readers-at-once proof. Two scenarios need none at all: the
upgrade deadlock has exactly one possible outcome for any thread on any
schedule, and `tryLock()`'s barging behaviour is a documented contract,
not a race. The throughput numbers above are real, measured, unforced
timings — the real JVM scheduler decided everything about how those
threads actually interleaved, and the numbers are what they are because
of it, not because anything pinned them.

## When this is too much

Worth it the moment the guarded work is substantial enough that letting
readers run in parallel genuinely pays for the lock's own coordination
cost — a larger computation, a slower lookup, anything past the trivial.
Not worth it for a value this cheap to copy: an immutable snapshot,
published atomically, gives every reader full parallelism with no lock
at all.
