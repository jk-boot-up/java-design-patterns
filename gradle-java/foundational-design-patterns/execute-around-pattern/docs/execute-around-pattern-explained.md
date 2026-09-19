# Execute Around, Explained

## The pattern in one sentence

Execute around puts the set-up and the clean-up in one method, and lets the caller hand in only the work in the middle.

## The six acts

### Open, Use, Close, By Hand

The query broke, and the code that would close the connection was after it. Connections still open: one. Repeat that on every failure, and the pool runs dry.

```
  the query broke, and the code that would close the connection was after it.
  connections still open: 1. repeat that on every failure, and the pool runs dry.
```

### The Caller Gives The Work

The same failure: the query broke. Connections opened: one. Still open: none. The closing is in one place, in a finally block, and cannot be forgotten.

```
  the same failure: the query broke.
  connections opened: 1, still open: 0. the closing is in one place, in a finally block, and cannot be forgotten.
```

### Getting An Answer Out

A string came out: the rows for an order. A number came out: fifteen. Still open: none.

```
  a string came out: rows for orders where id = 7. a number came out: 15. still open: 0.
```

### All Or Nothing

Two purchases of three thousand from a credit of five thousand: the second failed, with not enough credit. The balance afterwards is five thousand. The first purchase was undone too. One purchase of three thousand that works leaves two thousand.

```
  two purchases of 3000 from a credit of 5000: the second failed with "not enough credit".
  balance afterwards: 5000. the first purchase was undone too.
  one purchase of 3000 that works: balance 2000.
```

### The Same Shape, For Measuring

Receipt sent, in five ticks. And a failing job: the mail server timed out, and it was still measured: nine ticks.

```
  receipt sent in 5 ticks.
  and a failing job: mail server timed out, still measured: 9 ticks.
```

### The Bill

The caller let the connection out of the block, and used it later: connection one is closed. The block cannot stop that. The caller's code is now inside a lambda: it cannot return early, and it cannot throw a checked exception without help. And with two resources the blocks nest, one inside the other, so the real work drifts to the right.

```
  the caller let the connection out of the block, and used it later: connection 1 is closed. the block cannot stop that.
  the caller's code is now inside a lambda: it cannot return early, and it cannot throw a checked exception without help.
  and with two resources the blocks nest, one inside the other, so the real work drifts to the right.
```

## The verdict

Use execute around wherever something must be undone or finished after use: connections, files, locks, transactions, timers. Put the clean-up in a finally block, once. Do not let the resource leave the block. For plain files and streams, try-with-resources is the language's own form of it.

## How to recognise this in code you did not write

- `JdbcTemplate.query(...)` and `TransactionTemplate.execute(...)` in Spring.
- `try (var in = ...) { ... }`, the language's own version.
- `Files.lines` used inside a block, `lock.lock(); try { ... } finally { lock.unlock(); }`.
- A method that takes a lambda named `work`, `callback` or `action`.

## Where you have already met this

Spring's template classes, Hibernate sessions, the try with resources statement, and test frameworks that run set-up and tear-down around each test.

## When this is too much

For a resource used once, in one place, try with resources is enough. Write your own around method when many callers repeat the same set-up and clean-up.
