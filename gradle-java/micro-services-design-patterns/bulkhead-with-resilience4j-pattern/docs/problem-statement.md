# Problem Statement

## Read the partner first

This project assumes [Bulkhead](../bulkhead-pattern), which gave the nightly supplier feed and checkout their own pools of workers, so a slow partner API could fill the feed's pool without stopping the shop selling. Nothing here is lost by skipping Resilience4j, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: a slow supplier feed and a fast checkout, and whether one can starve the other.

## What is new

**Resilience4j** has the bulkhead built in, in two kinds: one that limits how many calls run at once, and one that gives the work its own threads.

```
  four slow feed jobs hold every permit. checkout is refused: BulkheadFullException.
  a background job stopped the shop selling.
```

## The failure this project exists to show

A call on `this` skips the limit. The wall between compartments wastes capacity. And which kind you choose decides whether a full compartment blocks the caller.
