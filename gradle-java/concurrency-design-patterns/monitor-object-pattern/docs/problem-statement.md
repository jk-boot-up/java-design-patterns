# Problem Statement

## The scenario

The store keeps one number per product: how many are in stock. Many
checkout threads reduce it, one sale at a time. A receiving thread adds
to it when a delivery arrives. A checkout that wants three items when two
are left should wait for the delivery rather than fail.

## The naive version, in three parts

### Part one: a plain count

Selling one item is three steps: read the count, subtract one, write the
result back. Two threads can both read ten, then both write nine.

```
ONE. A plain count — the lost update.
  stock started at 10; two checkout threads each sold one
  stock now: 9 — two items sold, one gone from the count.
```

Two items left the shelf. The count says one did. This project's
rendezvous makes it happen on every run.

### Part two: volatile

The popular half-fix is to mark the field `volatile`.

```
TWO. volatile — visible, but still not atomic.
  stock now: 9 — the same lost update, with volatile.
```

`volatile` promises that a write is seen by other threads. It does not
turn read, subtract, write into one step.

### Part three: the caller takes the lock

Put a lock beside the count and ask every caller to take it. It works
until one caller forgets.

```
THREE. The caller holds the lock — until one forgets.
  one caller took the lock; one forgot.
  stock now: 9 — the careful caller's lock protected nothing.
```

## What this project must deliver

An object that owns its own lock, so a caller cannot forget it, and owns
its own waiting, so a thread that needs stock can wait for the thread that
adds it. And it must say plainly what that costs.
