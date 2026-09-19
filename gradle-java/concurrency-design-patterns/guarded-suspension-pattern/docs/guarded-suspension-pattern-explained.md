# Guarded Suspension, Explained

## The pattern in one sentence

Guarded suspension makes a thread wait until a condition is true before it carries on, sleeping rather than asking again and again, and checking the condition again when it wakes.

## The six acts

### Waiting By Asking

The picker asks again and again whether an order has come. Before any order arrives it has asked more than a million times, keeping a processor busy for nothing.

```
  the picker asks whether an order has come, over and over. no order has come, and it has already asked more than a million times: true.
  it took [ORD-1] when it arrived. the whole time it kept a processor busy doing nothing.
```

### Waiting By Sleeping

The picker's thread is waiting, using no processor, and has asked nothing. An order arrives, the picker is woken and takes it.

```
  the picker's thread is: WAITING. it is using no processor, and has asked nothing.
  an order arrives, the picker is woken, and takes [ORD-1].
```

### Ask Again After Waking

Two pickers wait and one order arrives. With the guard checked by if, both wake, and one takes nothing. With while, the second picker looks again, finds nothing, and goes back to waiting.

```
  two pickers wait and one order arrives, with the guard checked with if: they took [ORD-1, null].
  two pickers wait and one order arrives, with the guard checked with while: they took [ORD-1].
  the second picker woke, looked, found nothing, and went back to waiting: true.
```

### The Order Came First

The order was already there, and its notification came and went. A picker that waits without looking first sleeps, though the order is waiting. A picker that checks the guard first takes it at once.

```
  the order was already there, and its notification has come and gone. a picker that waits without looking first: WAITING, holding nothing.
  a picker that looks at the guard first takes it at once: [ORD-1].
```

### Wait, But Not For Ever

With no order coming, the picker gives up after a hundred milliseconds and gets nothing. With an order there, it takes it at once.

```
  no order comes. after 100 milliseconds the picker gives up: null.
  with an order there: ORD-1.
  a limit turns 'wait until it is true' into 'wait a while, and tell me if it was not'.
```

### The Bill

Twenty pickers wait, and one order arrives. Notify all wakes all twenty, one takes it, and nineteen go back to sleep. And a thread waiting for something nobody will send waits forever.

```
  20 pickers waiting, 1 order arrives, and notifyAll: 20 threads woke, 1 took it, 19 went back to sleep.
  and a thread waiting for something nobody will ever send waits for ever. every wait needs a plan for how it ends.
```

## The verdict

Use guarded suspension when a thread cannot go on until a condition holds. Prefer a blocking queue or a condition object from the standard library to writing wait and notify yourself. If you do write it, check the guard in a while loop, before waiting and after waking, change the state under the same lock you wait on, and give the wait a limit.

## How to recognise this in code you did not write

- `while (!condition) { wait(); }`, or `condition.await()` in a loop.
- `BlockingQueue.take()`, `CountDownLatch.await()`, `Future.get()`.
- `notify` and `notifyAll` beside a state change.
- A `synchronized` method that starts with a `while`.

## Where you have already met this

`BlockingQueue`, `Future.get()`, `CountDownLatch`, and every thread pool waiting for work.

## When this is too much

Writing wait and notify by hand is rarely right when a blocking queue does it. And where the caller can give up, balking is simpler than waiting.
