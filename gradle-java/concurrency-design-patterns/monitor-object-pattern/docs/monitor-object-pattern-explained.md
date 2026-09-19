# Monitor Object, Explained

## The pattern in one sentence

The object owns its lock and its waiting: every public method takes the
lock itself, so the only way to use the object is the safe way.

## Why the earlier attempts fail

A plain count loses updates because read, subtract and write are three
steps. `volatile` fixes visibility, not atomicity. A lock held by the
caller fixes atomicity only for callers who remember it. Each fix moves
the responsibility, and a responsibility left to callers gets forgotten.

## The pattern

`StockMonitor` holds a `ReentrantLock` and a `Condition` as private
fields. `sellOne`, `take`, `add` and `available` each take the lock,
do their work, and release it in a `finally`. There is no public way to
touch the count without the lock.

Waiting lives inside too. `take(3)` waits on the object's own condition
until three items are in stock. `add(3)` signals it. The waiting thread
never polls and never sleeps.

```
FOUR. The pattern — the object owns its lock.
  8 threads x 25000 sales from 200000: 0 left, in 9ms
  a thread waited for 3 items, was signalled by the thread that added them,
  and took them: 0 left.
```

## The bill

**The lock is a bottleneck by design.** One thread is inside at a time.
That is what makes the object safe, and it is also its throughput limit.

**`wait` must sit in a loop.** A woken thread has been told stock may be
there, not that it is. With `if`, two woken takers both proceed and the
count goes to minus one.

```
FIVE. wait() in an if, not a while.
  with if:    stock ends at -1 — a sale of an item that was never there.
  with while: stock ends at 0, and 1 taker is still waiting, correctly.
```

**Two monitors can deadlock each other.** A thread holding one monitor and
asking for another, against a thread doing the reverse, waits forever.

**Calling out while holding the lock invites the same thing.** If the
monitor calls code it does not own, that code can ask another thread for
something that needs the lock the monitor is holding.

```
SIX. When a correct monitor still deadlocks.
  deadlock detected by the JVM: true, broken by interrupting both: true
  timed out: true, after 206ms
```

## What the scheduler really does

This project forces each failure by pinning one fact: both threads have
read before either writes, both takers are waiting before the item is
added, both threads hold their first lock before either asks for the
second. The scheduler still chooses everything else, including which
woken taker runs first. The throughput figure in act four is a real
measurement and changes from machine to machine. A passing test proves the
forced scenario, not safety under every schedule.

## When this is too much

For one counter, `AtomicInteger` is simpler and faster. The monitor earns
its place when several fields must change together, or when threads must
wait for a condition.
