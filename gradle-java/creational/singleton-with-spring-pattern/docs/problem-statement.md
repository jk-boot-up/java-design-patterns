# Problem Statement

## Read the partner first

This project assumes [Singleton](../singleton-pattern), which built an order-number sequencer that checkout, the admin console and a retry job must share, and closed the reflection and serialization holes with a single-element enum. Nothing here is lost by skipping Spring Boot, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: one order-number sequencer shared by checkout, the admin console and a retry job, so no two customers get the same number.

## What is new

Spring keeps **one instance per container** and hands it to whoever asks. The class itself is ordinary: a public constructor, no static field.

```
  checkout, admin and retry hold the same generator: true
  ORD-000001
  ORD-000002
  ORD-000003  (three callers, one counter)
```

## The failure this project exists to show

The guarantee moves from the language to the container. A second container, a changed scope, or a plain `new` gives a second counter, and two customers get the same order number.
