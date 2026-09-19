# Publisher-Subscriber, Explained

## The pattern in one sentence

Publisher-subscriber lets a service announce an event once, to a topic, and lets any number of other services listen, without the publisher knowing who they are.

## The six acts

### The Order Service Calls Each One

The order service calls inventory, email and analytics itself. It knows three services by name, and a fourth means editing it.

```
  inventory [ORD-1], email [ORD-1], analytics [ORD-1].
  the order service knows 3 services by name. a fourth, loyalty points, means editing it.
```

### The Order Service Only Publishes

The order service publishes once, and all three subscribers get the event. A fourth, loyalty points, is added, gets the event, and the order service is not changed.

```
  inventory [ORD-1], email [ORD-1], analytics [ORD-1].
  a fourth subscriber, loyalty points, is added: [ORD-1]. the order service was not changed.
```

### Each At Its Own Pace

Five orders are published. Email handles all five, and analytics only one, with a backlog of four. Analytics catches up later, without holding up email or the publisher.

```
  5 orders published. email handled 5, analytics handled 1. backlog of email: 0, of analytics: 4.
  analytics catches up later: handled 5, backlog 0. a slow subscriber did not hold up the fast one, or the publisher.
```

### Each Takes What It Wants

Email asks only for placed orders and gets one. Analytics asks for everything and gets a placed and a cancelled event.

```
  email asked only for placed orders: [OrderPlaced ORD-1].
  analytics asked for everything: [OrderPlaced ORD-1, OrderCancelled ORD-1].
```

### A Subscriber That Arrives Late

Three orders were published before loyalty joined, and one after. A live subscriber sees only the last. One that reads from the start sees all four, because the log was kept.

```
  3 orders were published before loyalty was added, and one after.
  a subscriber that joins live sees: [ORD-4]. one that reads from the start sees: [ORD-1, ORD-2, ORD-3, ORD-4].
  keeping the log is what makes a late subscriber possible, and it has to be kept somewhere.
```

### The Bill: Nobody Knows Who Got It

Email is down when the order is placed, and the publisher is told nothing. When it comes back it catches up, because its place in the log was kept. The publisher still cannot ask whether the email went out.

```
  email was down when the order was placed. the publisher was told: nothing. email got: [], backlog 1.
  when it came back, it caught up: [ORD-1]. because its place in the log was kept.
  the publisher still cannot ask whether the email went out. it published, and it does not know who listened.
```

## The verdict

Use publish and subscribe when one thing happens and several independent parties care, and when new parties will come along. Keep the events small and named for what happened. Keep the log long enough for a late or absent subscriber. Make every subscriber safe to run twice. Do not use it when the publisher needs an answer.

## How to recognise this in code you did not write

- A `publish` call with a topic name and no reference to any consumer.
- Kafka topics and consumer groups, SNS topics, Google Pub/Sub, RabbitMQ fanout exchanges.
- `ApplicationEventPublisher` and `@EventListener` in Spring, inside one process.
- A subscription with a filter or a routing key.

## Where you have already met this

Every event-driven system, and the browser's `addEventListener`.

## When this is too much

If one known service needs the result, a direct call is clearer. A topic is for facts that many may want, and that you do not want to track.
