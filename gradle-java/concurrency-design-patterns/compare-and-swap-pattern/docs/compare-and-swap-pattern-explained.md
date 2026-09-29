# Lock-Free Compare-and-Swap, Explained

## The pattern in one sentence

Compare-and-swap changes a value only if it still holds what the thread saw,
and otherwise retries, giving correct updates to a single value with no locks.

## The 5 acts

### 1. Check, then act

`UnsafeStock.buyOne` reads the count, runs a quick fraud check, then writes
back the count minus one. Two buyers read the same count during each other's
fraud check, and both write back the same new value: one kettle counted,
two sold. With eight buyers the shop sells more than 100 kettles from a stock
of 100.

### 2. A lock

`LockedStock.buyOne` is `synchronized`: only one buyer at a time may look and
take. Exactly 100 kettles are sold and none are left. It is correct, but every
other buyer waits in line during each fraud check.

### 3. Compare-and-swap

`CasStock.buyOne` reads the count, runs the fraud check, then calls
`compareAndSet(seen, seen - 1)`: take one only if the count is still what it
saw. If another buyer got there first, the swap fails and the buyer reads
again. Exactly 100 are sold, none left, and no thread ever waited for a lock.

### 4. The loop in one call

Java's atomic classes hide the retry loop: `getAndUpdate` takes a function
from old value to new, and retries the compare-and-swap for you. The flash
sale again sells exactly 100.

### 5. The bill

Compare-and-swap protects one value. Taking a kettle and recording the buyer
are two separate atomic values; a thread that stops between them leaves stock
at 99 and no buyer recorded. And under heavy contention, threads spin
retrying instead of waiting quietly.

## The verdict

Use atomic classes for single shared values: counters, stock levels, flags,
references. Prefer `updateAndGet` to hand-written loops, use `LongAdder` for
hot counters, and use a lock or transaction when several values must change
together.

## How to recognise this in code you did not write

- `AtomicInteger`, `AtomicLong`, `AtomicReference` fields.
- `while (true) { ... if (x.compareAndSet(a, b)) return; }` loops.
- `version` columns checked in database updates.

## Where you have already met this

- `AtomicInteger.incrementAndGet`, `compareAndSet`, `updateAndGet`.
- `ConcurrentHashMap` and `ConcurrentLinkedQueue`, built on compare-and-swap.
- Optimistic locking in databases: `UPDATE ... WHERE version = 7`.
- Git's refusal to push when the remote branch moved since you last pulled.
