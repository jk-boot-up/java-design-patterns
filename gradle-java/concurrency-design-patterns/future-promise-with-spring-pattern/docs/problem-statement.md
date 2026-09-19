# Problem Statement

## Read the partner first

This project assumes [Future/Promise](../future-promise-pattern), which built the Future and Promise handoff by hand, and showed three costs: an exception surfaces later with a stack trace that omits the caller, a bare `get()` is a hang, and cancellation is a request a task can ignore. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: a product page needs three independent lookups, price, stock and a review score, and none depends on the others.

## What is new

`@Async` on a method that returns a `CompletableFuture` runs it on the container's pool and hands back the future. The container is the promise: it completes the future when the method returns, or fails it when the method throws.

```
  on the default pool, lookups in flight at the same moment: 3
  on a pool of one thread: 1
```

## The failure this project exists to show

Four things `@Async` does not do for you: the pool decides how concurrent it is, a `void` method's exception is lost, thread-locals do not cross the thread boundary, and neither a timeout nor `cancel(true)` stops the work.
