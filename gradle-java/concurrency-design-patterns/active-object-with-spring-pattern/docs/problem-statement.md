# Problem Statement

## Read the partner first

This project assumes [Active Object](../active-object-pattern), which built an object with its own thread and mailbox by hand, so calls became messages that return a future at once, with no lock, and showed its costs: a mailbox that backs up, errors that arrive later with the worker's stack, and a throughput ceiling. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: inventory updates arrive from checkout, returns and a slow import, and a monitor made checkout wait behind the import.

## What is new

An `@Async` bean on a **one-thread executor** is an active object. The executor's queue is the mailbox, the future is the reply, and the state is a plain field that only that one thread touches.

```
  4 callers x 5000 restocks: stock 20000
  the stock field is a plain int: no lock, not volatile.
```

## The failure this project exists to show

The guarantee is only as good as the discipline of routing every access through the proxy. One call on `this` changes the field from the wrong thread and an update is lost, and a getter that reads the field directly sees the past.
