# Problem Statement

## The scenario

Every query to the order database needs a connection, and every connection must be closed, whether the query works or fails.

## The naive version

Every caller opens a connection, uses it, and closes it, in its own code.

```
  the query broke, and the code that would close the connection was after it.
  connections still open: 1. repeat that on every failure, and the pool runs dry.
```

## What this project must deliver

A pool that counts open connections; a hand-over version that leaks after a failure; an around method that closes in a finally block; results that come out with generics; a ledger transaction that undoes all its steps on failure; a timer with a fake clock; and a connection that escapes the block.
