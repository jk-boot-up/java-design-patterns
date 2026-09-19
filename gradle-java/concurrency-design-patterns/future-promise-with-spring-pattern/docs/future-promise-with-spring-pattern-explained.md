# Future/Promise with Spring, Explained

## The pattern in one sentence

`@Async` returns a `CompletableFuture` that the container completes, so independent work can run at once, on a pool you must choose.

## What is new here

The pattern is [Future/Promise](../future-promise-pattern). This page is only what Spring Boot adds.

### The Pool Decides

`@Async` asks for concurrency and the pool decides whether to give it: three lookups overlap on the default pool, and on a pool of one thread they run one at a time.

```
  on the default pool, lookups in flight at the same moment: 3
  on a pool of one thread: 1
```

### Exceptions

A method returning a future carries its exception to the caller, with a stack trace that belongs to a pool thread. A `void` method's exception reaches nobody: only a handler you register by hand.

```
  a method returning a future: the caller sees CompletionException, cause "the review service is down".
  the calling method appears in that stack trace: false.
  a void method threw, and the caller got: nothing.
  the only place it went is a handler you have to register
```

### Thread-Locals

Request context, security context and logging context are thread-locals, and none crosses to a pool thread. A `TaskDecorator` bean that copies it is the fix, and it is yours to write.

```
  the caller is working for customer 7. the async method asked whose order it is: "customer null".
  with a TaskDecorator that copies it across: "customer 7".
```

### A Timeout Does Not Stop It

`orTimeout` makes the caller give up. The task keeps running, and finishes its work, with nobody waiting for the answer.

```
  the caller waited 200ms and got: TimeoutException.
  the task had finished when the caller gave up: false.
  and then it ran to the end anyway, and did its work: true.
```

### cancel(true) Interrupts Nothing

`cancel(true)` on a `CompletableFuture` sets a flag on the future. It never interrupts the thread, so the task runs to completion.

```
  cancel(true) reported: true. isCancelled: true.
  the task ran to completion anyway: true.
```

### Composing The Page

Three futures combine into a page with no `get` until the end. One failing lookup fails the whole page unless a fallback is chosen at that one step.

```
  assembled from three futures, with no get() until the end: price £129.99, stock 7, rating 4.6
  with the review service down and a fallback chosen at that one step: price £129.99, stock 7, rating unavailable
```

## The verdict

Return a `CompletableFuture`, never `void`. Choose the pool. Propagate context on purpose, with a `TaskDecorator`. Treat a timeout as giving up, not stopping, and design tasks that check for cancellation themselves.

## How to recognise this in code you did not write

- `@Async` on a method returning `CompletableFuture`.
- `.thenCombine`, `.exceptionally` and `.orTimeout` chains in a service.
- A `TaskDecorator` or `AsyncUncaughtExceptionHandler` bean.
- `MDC` or `SecurityContextHolder` copied by hand across a thread.

## Where you have already met this

Every `@Async` method that returns a `CompletableFuture`, and every log line that lost its request id on the way to a pool thread.

## When this is too much

For two lookups that are already fast, or where the second needs the first's result, a future around work that never overlaps is ceremony.
