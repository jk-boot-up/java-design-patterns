# Thread Pool with Spring, Explained

## The pattern in one sentence

Spring's `@Async` runs a method on a pool of threads the container owns, so the shape of that pool is a setting you must choose.

## What is new here

The pattern is [Thread Pool](../thread-pool-pattern). This page is only what Spring Boot adds.

### What You Get By Default

With `@EnableAsync` and no settings, the executor is a `ThreadPoolTaskExecutor` with eight core threads and a queue with no bound: the partner's unbounded-queue trap, as a default.

```
  core threads 8, max threads 2147483647, queue capacity 2147483647.
  eight workers, and a queue with no bound.
```

### @Async Moves The Work

One annotation replaced the partner's `BoundedPackingPool` class: the method runs on a pool thread, not the caller's.

```
  the caller is thread "main". the work ran on "task-1".
```

### The Unbounded Queue

Eight workers stuck on a slow step, and a thousand more orders arrive. All thousand wait, none is refused, and nobody is told. The backlog grows until it is a heap dump instead of a decision.

```
  all 8 workers are stuck on a slow step. 1000 more orders arrive.
  waiting in the queue: 1000. rejected: 0. nobody was told.
```

### Bound It

Three properties bound the pool. The sixth order is refused with a real `TaskRejectedException`, thrown to the caller at once. That is a decision: the caller learns the pool is full.

```
  three settings: 2 threads, a queue of 3. two orders are running and three are waiting.
  the sixth order: TaskRejectedException, thrown to the caller, at once.
```

### The Annotation That Does Nothing

`@Async` works through a proxy. A call from one method of a bean to another goes to `this`, skips the proxy, and runs on the caller's thread. Nothing complains.

```
  packThroughThis() called pack(), which is @Async, through this. it ran on "main", the caller's own thread.
```

### Pool Starvation

With one thread, a task that asks its own pool for a label and waits for it can never finish: the label task is queued behind it. The same deadlock as the partner's act five.

```
  one thread. the packing task asks the pool to print a label, and waits for it.
  starved: the label task never got a thread
```

## The verdict

Set the pool explicitly, bound the queue, decide what a refusal means, and never wait on your own pool. Do not rely on the default executor for anything that can back up.

## How to recognise this in code you did not write

- `@EnableAsync`, and methods annotated `@Async`.
- `spring.task.execution.pool.*` properties, or a `ThreadPoolTaskExecutor` bean.
- `TaskRejectedException` in a stack trace.
- A `CompletableFuture` returned from a service method.

## Where you have already met this

Every `@Async` method, and Spring Boot's `applicationTaskExecutor`. `@Scheduled` and `@EventListener` with `@Async` use the same kind of pool.

## When this is too much

For work that is already fast, or that must finish before the caller continues, a thread pool is only overhead.
