# Active Object with Spring, Explained

## The pattern in one sentence

An `@Async` bean on a one-thread executor is an active object: calls become messages, and one thread owns the state.

## What is new here

The pattern is [Active Object](../active-object-pattern). This page is only what Spring Boot adds.

### No Lock At All

Four callers restock a plain `int` twenty thousand times in all, and the total is exact. There is no lock: every change ran on the one `inventory-` thread.

```
  4 callers x 5000 restocks: stock 20000
  the stock field is a plain int: no lock, not volatile.
```

### The Mailbox

The executor's queue is the mailbox. With the worker busy, ten thousand messages wait and none is refused. Bound the queue to three and the fourth waiting message is refused with `TaskRejectedException`.

```
  messages waiting in the mailbox: 10000. nothing refused them.
  with a mailbox of 3: the fourth message waiting is refused with TaskRejectedException.
```

### A Call That Skips The Proxy

The guarantee holds only for calls through the proxy. A call on `this` changes the field on the caller's thread while the worker is mid-change, and the worker then writes over it.

```
  the worker read the stock (0) and is holding it. a caller adds 5 through this, on its own thread: stock 5.
  the worker then writes 0 + 10. final stock: 10, not 15. five items vanished.
```

### A Read That Skips The Mailbox

A direct getter reads the field on the caller's thread and sees the state before the queued restock. A read sent as a message waits its turn and sees the restock. In an active object, reads are messages too.

```
  a getter that reads the field directly, from the caller's thread, says: 0.
  a read sent as a message, behind the restock, says: 5.
```

### Errors Arrive Later

A failing message fails its future later, with the worker's stack. The method that sent it appears nowhere in the trace.

```
  cause: stock feed unavailable [raised on inventory-1]
  the calling method appears nowhere in that trace: true.
```

### One Worker Is A Ceiling

With each message costing fifty microseconds of work, one caller and four callers get the same rate: the ceiling is the worker.

```
  1 caller:  19034 per second
  4 callers: 19432 per second
  four times the callers, the same rate: the ceiling is the worker.
```

## The verdict

Use it when callers must not wait and one owner for the state is enough. Route every access, reads included, through the proxy. Bound the mailbox. Never give the executor a second thread.

## How to recognise this in code you did not write

- `@Async("someExecutor")` with an executor whose core and max size are 1.
- A service with mutable fields and no `synchronized`, whose methods all return futures.
- A `Single`-thread executor named for the thing it protects.
- A comment saying "only ever called from the worker thread".

## Where you have already met this

A single-thread executor named for the thing it protects, and every `@Async("name")` method that uses it. Actor libraries take this idea much further.

## When this is too much

For state that changes rarely, a plain synchronized method is simpler. An active object earns its place when callers must not wait.
