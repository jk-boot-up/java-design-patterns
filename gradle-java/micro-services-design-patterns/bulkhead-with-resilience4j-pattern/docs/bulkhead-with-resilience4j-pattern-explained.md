# Bulkhead with Resilience4j, Explained

## The pattern in one sentence

In Resilience4j, a bulkhead is an annotation that limits how many calls to one thing may run at once, or that gives them their own threads.

## What is new here

The pattern is [Bulkhead](../bulkhead-pattern). This page is only what Resilience4j adds.

### One Compartment For Everything

Four slow feed jobs hold every permit of one shared compartment, so checkout is refused.

```
  four slow feed jobs hold every permit. checkout is refused: BulkheadFullException.
  a background job stopped the shop selling.
```

### A Compartment Each

The feed has two permits of its own. Two slow jobs fill it, a third is refused, and checkout, in its own compartment, still sells.

```
  a third feed job is refused: BulkheadFullException.
  checkout while two feed jobs are stuck: sold.
```

### What A Full Compartment Does

A full compartment refuses at once. With a fallback method the refused job gets an answer instead of an exception.

```
  with a fallback method, the third feed job gets: feed batch skipped tonight.
```

### The Cost Of The Wall

The feed compartment is full while checkout's four permits sit unused. The wall keeps them apart.

```
  permits free in the feed compartment: 0. in the checkout compartment: 4.
  checkout's four permits cannot help the feed, even now.
```

### The Annotation Is A Proxy

Ten feed jobs called through this are all inside at once, in a compartment of two. The bulkhead never saw them.

```
  10 feed jobs called through this, in a compartment of 2. all 10 are inside at once.
  permits free in the feed compartment: 2. it never saw them.
```

### A Compartment With Its Own Threads

The thread-pool kind runs each call on its own threads: two running, one queued, and the fourth refused. The caller returns at once every time.

```
  four submissions, and the caller was never blocked. running: 2. waiting in the queue: 1.
  the fourth was refused: BulkheadFullException.
  the first ran on: bulkhead-feedpool-N. all three finished: true.
```

## The verdict

Give each kind of work its own compartment, and size them from real load. Choose the thread-pool kind when a full compartment must not block the caller. Never call a bulkhead method on this. Watch the free permits.

## How to recognise this in code you did not write

- `@Bulkhead(name = ...)` and `type = Bulkhead.Type.THREADPOOL`.
- `resilience4j.bulkhead.instances.*` and `resilience4j.thread-pool-bulkhead.instances.*`.
- `BulkheadFullException` in a log.

## Where you have already met this

Any Spring service that calls several other services, some of them slow.

## When this is too much

For one caller and one dependency, the limit is a rate limiter's job, not a compartment's.
