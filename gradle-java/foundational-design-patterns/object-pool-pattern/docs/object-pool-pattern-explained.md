# Object Pool, Explained

## The pattern in one sentence

Keep a few expensive objects, lend them out, and take them back.

## The one place it is right

The connection is expensive to create, and the expense is **outside the JVM**: a
network handshake. Pooling it saves eighty per cent of the time in act two. The
same is true of threads and native handles. A connection pool is this pattern,
and so is a [thread pool](../../concurrency-design-patterns/thread-pool-pattern),
the pattern's other unambiguously correct use.

## The bill

### On a modern JVM, allocation is cheap

Pooling an ordinary object is almost always a pessimisation.

```
THREE. The bill: pooling a small object is slower than allocating it.
  allocating (the JIT may remove it entirely): 0.35 ns per operation
  allocating (forced onto the heap):           2.19 ns per operation
  borrowing from a pool:                       6.44 ns per operation
  the pool is 2.9 times slower than real allocation.
  objects created: 20000000 by allocating, 4 by pooling.
```

The pool creates almost no objects and still loses on time, because it adds a lock
and moves objects through shared memory, while the JVM's allocator is a pointer
bump in a thread-local buffer.

### How the benchmark was measured

This is a hand-rolled measurement, not JMH, and the method is written down so it
can be checked.

- Each variant does the same work per operation: fill a three-field object and add
  its total to a running sum, which is read at the end so the work cannot be
  optimised away.
- The pool is a synchronised `ArrayDeque`, the simplest thread-safe pool there is,
  used here from one thread.
- Five warm-up rounds are discarded. Nine measured rounds follow, and the
  **median** per-operation time is reported. The variants alternate in each round.
- Allocation is measured twice. As plain code, the JIT's escape analysis may
  remove the allocation entirely, which is why it can read under a nanosecond. A
  knowledgeable reader will rightly say that is not a fair comparison, so it is
  also measured with every object stored in a static field, which forces a real
  heap allocation. **The pool is compared against that one.**
- Absolute numbers depend on the machine. The direction, and the ratio of roughly
  three, were stable across repeated runs. A pool with no lock would be faster than
  this one and still would not beat allocation. Multithreaded contention makes a
  shared pool worse, not better.

### A returned object carries its old state

```
FOUR. The bill: a returned object carries its old state.
  the connection says its last card holder was: Ada Lovelace
  with a reset on return: null. every pool needs one.
```

A security bug, not a performance one, and the one that happens in the field.

### A leaked object is never returned

```
FIVE. The bill: a leaked object is never returned.
  a third payment waited 310ms and got: nothing (rescued by a timeout)
```

Without the timeout it waits forever. That is worse than a slow start.

### Sizing is a guess

```
SIX. The bill: sizing is a guess, and both directions cost.
  pool of 1:  218ms (they queue)
  pool of 4:  58ms
  pool of 50: 50 connections opened, and 46 sit idle
```

## The verdict

Pool things that are expensive **outside** the JVM: connections, threads, native
handles. Pool nothing else.

## How to recognise this in code you did not write

- A class called `...Pool`, with `borrow`/`acquire` and `release`/`return`.
- `HikariCP`, `commons-dbcp` and every JDBC `DataSource`: connection pools.
- `ExecutorService`: a pool of threads.
- A `Stack` or `Queue` of reusable objects with a `reset()` call, in code that
  claims to be avoiding garbage collection.

## Where you have already met this

Every database `DataSource` you have configured is one.

## When this is too much

For anything cheap to create, which is nearly everything.
