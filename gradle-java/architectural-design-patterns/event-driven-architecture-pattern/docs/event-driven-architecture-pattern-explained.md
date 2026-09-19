# Event-Driven Architecture, Explained

## The pattern in one sentence

Event-driven architecture builds a system out of services that do not call each other, but write facts to a shared log, and read the log at their own pace.

## The six acts

### Calling And Waiting

The order service calls shipping and waits. Shipping is down. The order is not accepted. A customer lost an order because a service they never see was down.

```
  the order service calls shipping and waits. shipping is down. order accepted: false. orders placed: 0.
  a customer lost an order because a service they never see was down.
```

### Telling The Log

The order service appends the event at position zero, and finishes. It has no reference to inventory or shipping. Both read the log, and both act.

```
  the order service appended the event at offset 0 and finished. it has no reference to inventory or shipping.
  [inventory reserved ORD-1, shipping planned ORD-1].
```

### A Service That Is Down

Shipping is down. Three orders are accepted anyway. Shipping has planned nothing, and is three events behind. When it comes back, it catches up, and plans all three.

```
  shipping is down. three orders were accepted anyway. shipping planned [], and is 3 events behind.
  shipping came back and caught up: planned [ORD-1, ORD-2, ORD-3], 0 behind.
```

### A New Reader

Analytics is added after two orders. It reads the log from the start, and sees both. The order service was not touched.

```
  analytics was added after two orders. it read the log from the start: [ORD-1, ORD-2].
  the order service was not touched. the log is kept, so a new service can be built from history.
```

### Not The Same Instant

The order is accepted, and stock in the warehouse is still ten. It should be nine. After inventory reads the log, it is nine. For a moment, the two disagree. The system is eventually consistent, not consistent at every instant.

```
  the order is accepted. stock in the warehouse: 10. it should be 9.
  after inventory reads the log: 9.
  for a moment the two disagree. the system is eventually consistent, not consistent at every instant.
```

### The Bill

The same event is delivered twice. Without a duplicate check, stock is eight. With one, it is nine, which is right. And the flow of an order is now spread over several services. To see it, you read the log, not one piece of code.

```
  the same event delivered twice. stock: without a duplicate check 8, with one 9. it should be 9.
  and the flow of an order is now spread over several services, each reading the log: to see it, you read the log, not one piece of code.
```

## The verdict

Use events when services should not depend on each other being up, and when new services will come. Keep the log. Expect eventual consistency, and design for it. Make every reader safe to repeat. And keep a way to see the whole flow, because no single piece of code shows it.

## How to recognise this in code you did not write

- Kafka, Pulsar, Kinesis or a similar log at the centre of a system.
- Services whose only link is a topic name.
- Event sourcing, and CQRS read models built by reading events.
- Consumers with an offset or a lag metric.

## Where you have already met this

Kafka-based systems, Amazon's order pipelines, and the browser, where everything is an event.

## When this is too much

For a small system where all parts are always up together, a direct call is simpler and easier to follow. Events pay off when parts fail or change on their own.
