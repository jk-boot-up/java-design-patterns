# Problem Statement

## Read the partner first

This project assumes [Thread Pool](../thread-pool-pattern), which built a bounded thread pool by hand around a `ThreadPoolExecutor`, and showed its costs: an unbounded queue is a trap, a rejected task needs a decision, and a pool can starve itself. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: orders arrive to be packed, and packing is slow. Something must decide how many orders are packed at once, and what happens to the rest.

## What is new

One annotation, `@Async`, sends a method to a thread pool the container owns. The pool's shape is not code. It is configuration, and its defaults matter.

```
  core threads 8, max threads 2147483647, queue capacity 2147483647.
  eight workers, and a queue with no bound.
```

## The failure this project exists to show

The defaults are the partner's unbounded-queue trap. And the annotation, like `@Transactional`, works through a proxy, so a call on `this` skips it and nothing complains.
