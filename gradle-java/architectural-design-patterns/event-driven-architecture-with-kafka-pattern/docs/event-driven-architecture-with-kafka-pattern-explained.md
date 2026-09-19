# Event-Driven Architecture with Kafka, Explained

## The pattern in one sentence

With Kafka, the log is a topic on a broker, and each service reads it as a consumer group that the broker remembers.

## What is new here

The pattern is [Event-Driven Architecture](../event-driven-architecture-pattern). This page is only what Apache Kafka adds.

### Calling And Waiting

The order service calls shipping and waits. Shipping is down. The order is not accepted. A customer lost an order because a service they never see was down.

```
  the order service calls shipping and waits. shipping is down. order accepted: false. orders placed: 0.
  a customer lost an order because a service they never see was down.
```

### Telling The Log

The order service sends the event to Kafka, which gives it offset zero, and it finishes. It has no reference to inventory or shipping. Both read the topic, and both see the order.

```
  the order service sent the event to Kafka, which gave it offset 0, and finished. it has no reference to inventory or shipping.
  [inventory saw OrderPlaced ORD-1, shipping saw OrderPlaced ORD-1].
```

### A Service That Is Down

Shipping read the first order, and then went down. Three more orders were accepted. Shipping is three events behind, as the broker counts it. Shipping came back and caught up, from where it stopped. It has now planned four orders, and is none behind.

```
  shipping read ORD-1 and then went down. three more orders were accepted. shipping is 3 events behind, as the broker counts it.
  shipping came back and caught up, from where it stopped. it has now planned 4 orders, and is 0 behind.
```

### A New Reader

Analytics is added after two orders. It reads the topic from the start, and sees both. The order service was not touched. Kafka keeps the events, so a new service can be built from history.

```
  analytics was added after two orders. it read the topic from the start: [OrderPlaced ORD-1, OrderPlaced ORD-2].
  the order service was not touched. Kafka keeps the events, so a new service can be built from history.
```

### Not The Same Instant

The order is accepted, and stock in the warehouse is still ten. It should be nine. After inventory reads the topic, it is nine. For a moment, the two disagree. The system is eventually consistent, not consistent at every instant.

```
  the order is accepted. stock in the warehouse: 10. it should be 9.
  after inventory reads the topic: 9.
  for a moment the two disagree. the system is eventually consistent, not consistent at every instant.
```

### The Bill

The same event is delivered twice, as Kafka may after a missed commit. Without a duplicate check, stock is eight. With one, it is nine, which is right. The flow of an order is now spread over several services, so to see it, you read the topic, not one piece of code. And a broker is another system to run.

```
  the same event delivered twice, as Kafka may after a missed commit. stock: without a duplicate check 8, with one 9. it should be 9.
  and the flow of an order is now spread over several services, each reading the topic: to see it, you read the topic, not one piece of code.
  and a broker is another system to run: this demo needed 1 container for 1 topic.
```

## The verdict

Use a broker when services must not depend on each other being up, and when new services will come. Give each service its own group. Expect readers to be behind, and design for it. Make every reader safe to repeat. And watch the lag.

## How to recognise this in code you did not write

- `KafkaProducer` and `KafkaConsumer`, or `@KafkaListener`.
- A `group.id` for each service.
- Lag dashboards, and `kafka-consumer-groups.sh`.
- Topics named for facts in the past tense.

## Where you have already met this

Most large event-driven systems: order pipelines, activity feeds and change data capture.

## When this is too much

For a small system where all parts are always up together, a direct call is simpler. A broker is a system to run, and to understand.
