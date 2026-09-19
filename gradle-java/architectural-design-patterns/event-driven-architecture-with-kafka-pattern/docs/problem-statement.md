# Problem Statement

## Read the partner first

This project assumes [Event-Driven Architecture](../event-driven-architecture-pattern), which showed services that write facts to an append-only log and read it at their own pace, with a service that is down catching up, a new reader replaying history, briefly wrong stock, and a duplicate delivery absorbed by a check. Nothing here is lost by skipping Apache Kafka, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: an order service, and inventory, shipping and analytics reading its events.

## What is new

**Apache Kafka**, a real broker in a Docker container, holding the log, remembering each service's offset, and counting its lag.

```
  the order service calls shipping and waits. shipping is down. order accepted: false. orders placed: 0.
  a customer lost an order because a service they never see was down.
```

## The failure this project exists to show

The log is now another system to run. Delivery can repeat, so every reader must be safe to repeat. And nothing is instant: the readers are behind by design.
