# Backpressure with Project Reactor, Explained

## The pattern in one sentence

With Reactor, backpressure is built in: subscribers state their demand, and
sources that cannot honour it must buffer, drop or keep the latest.

## The 5 acts

### 1. A source that ignores demand

The supplier's feed pushes all ten thousand products at once, ignoring how many
the indexer asked for. The indexer's queue holds 256. Reactor does not let the
pile grow: it stops the stream with an OverflowException, and only part of
the feed is indexed. The rest is refused, not quietly piled up in memory.

### 2. Produce only what is asked

A feed that can wait, here `Flux.range`, produces only what is requested. The
indexer asks for ten, indexes them, then asks for ten more. All ten thousand
are indexed, and never more than ten were asked for and not yet delivered.

### 3. limitRate

`limitRate(10)` does the asking for you. The feed sees a request for ten, then
requests for eight each time three-quarters of the batch has been used, so
the next batch is on its way before the last one runs out.

### 4. Only the latest

A thousand stock-level updates for one mug arrive while the shop asks for just
one. `onBackpressureLatest` keeps only the newest one waiting. The shop asks
twice and gets two values: the first update, a thousand, and the latest, one.
The 998 in between were dropped, because only the current level matters.

### 5. The bill

Every source must choose. One that can wait, such as a range, a generator or a
database cursor, is simplest. One that cannot must buffer, costing memory, or
drop or keep the latest, losing data; Reactor makes you say which. And an
unbounded `onBackpressureBuffer()` just moves the pile somewhere harder to see.

## The verdict

Prefer sources that can wait. Let operators such as `limitRate` manage demand,
and for sources that cannot wait, choose a bounded buffer, a drop or the latest
on purpose.

## How to recognise this in code you did not write

- `Flux.create(..., OverflowStrategy.X)`.
- `.limitRate(n)`, `.onBackpressureLatest()`, `.onBackpressureBuffer(n)`.
- `BaseSubscriber` with `request(n)`.

## Where you have already met this

- Spring WebFlux, built on Reactor.
- RxJava, Akka Streams and Kotlin Flow, with the same ideas.
- The Reactive Streams interfaces, also in the JDK as `java.util.concurrent.Flow`.
