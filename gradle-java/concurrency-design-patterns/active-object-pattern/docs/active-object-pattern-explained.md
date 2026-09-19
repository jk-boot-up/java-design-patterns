# Active Object, Explained

## The pattern in one sentence

The object gets its own thread: calls become messages in its mailbox and
return a future at once, and because one thread owns the state, there is
no lock at all.

## What it is made of

A queue, a thread, a future, and state that one party owns. If any of
those is unfamiliar, read the project that teaches it first. This page only
covers what the assembly adds.

## How it works

`InventoryActiveObject` keeps a plain `int` field, not volatile and not
locked. Only its worker thread ever touches it. `reserve`, `restock` and
`importCorrection` do not touch it either. Each one packs the change into a
message, puts the message in the mailbox, and returns a `CompletableFuture`
at once. The worker takes messages one at a time, in order, applies each,
and completes its future.

```
TWO. An active object — the call returns at once.
  the import is running. reserve(1) has already returned.
  its result is ready yet: false
  import done: stock 50
  reserve done, later, in order: stock 49
```

Mutual exclusion comes from there being exactly one worker.

```
THREE. No lock at all — one thread owns the state.
  4 callers x 25000 restocks: stock 100000
```

## The bill

**Everything is asynchronous, including errors.** A failing message fails
its future, later, and the stack trace shows the worker, not the caller.

```
FIVE. Errors arrive later, from the worker.
  cause: stock feed unavailable [raised on inventory-worker]
  the calling method appears nowhere in that trace: true
```

**The mailbox can back up.** Nothing refuses a message and nothing slows
the sender down. If the worker is slower than its callers, the queue grows.

```
FOUR. The mailbox backs up.
  messages waiting in the mailbox: 10000
```

**One worker is a hard ceiling.** More callers do not make it faster.

```
SIX. One worker is a ceiling.
  1 caller:  4000 messages in 201ms, 19832 per second
  4 callers: 4000 messages in 200ms, 19919 per second
```

## What the scheduler really does

The harness pins what the scenario needs: the worker is parked on a gate
before the checkout call is made, the mailbox is counted while the worker
is held, and the failing message is thrown on the worker. The JVM still
decides when each caller's thread runs. The rates in act six are real
measurements and change between machines.

## Where this leads

Actors, in systems such as Akka, are active objects with mailboxes as their
main feature. Event loops, as in Node.js or Netty, are one worker with a
mailbox. This project names them and teaches neither.

## When this is too much

For state that changes rarely, a monitor is simpler. An active object earns
its place when callers must not wait, or when the work is slow.
