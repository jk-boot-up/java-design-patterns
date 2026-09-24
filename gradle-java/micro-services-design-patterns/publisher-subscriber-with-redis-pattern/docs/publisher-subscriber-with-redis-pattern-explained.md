# Publisher-Subscriber with Redis, Explained

## The pattern in one sentence

One part of a system announces that something happened, once, to a named place, and any number of other parts listen there — without the one announcing ever knowing who they are.

## The analogy, before any of Redis's words

Think of a live radio station. The presenter speaks once, and every radio tuned in at that moment hears it. The presenter does not know who is listening, and does not need to.

Now three things a radio station makes you face, which the partner project never had to. If your radio was off, there is no recording: you missed it. The station can know roughly how many radios were tuned in, but not whose they were, or whether anybody wrote anything down. And a radio that stops playing does not slow the station down. In Redis there is one more twist, best told with a kitchen: plates a table has not collected pile up on a shelf by the door, one shelf per table, and when a shelf overflows, the kitchen stops serving that table altogether.

## What Redis calls these things

**Redis** is a server that keeps data in memory and answers over the network. This project uses only its live-announcement feature, running in a container the demo starts and stops.

**Publishing** is speaking once: handing Redis one message under a name. Redis answers with a number — how many listeners it handed the message to, at that instant.

A **channel** is the name the message goes out under, like a radio frequency. Here the names are `orders.placed` and `orders.cancelled`. A channel is not stored anywhere; it exists only while somebody is listening on it.

**Subscribing** is tuning in: asking Redis to send you everything published under a name, from now on. A connection that is subscribed can do nothing else, so every subscriber in this project has its own connection.

A **pattern subscription** is tuning in by a shape rather than an exact name: `orders.*` hears every channel whose name starts with `orders.`.

The **client output buffer** is the shelf by the kitchen door: the pile of messages Redis has sent a listener but the listener has not read yet. Redis keeps one per connection, and it has a limit. For a subscriber, out of the box, the limit is 32mb, or 8mb if that lasts for 60 seconds. Past it, Redis closes the connection.

## The six acts

### The Order Service Calls Each One

The order service calls inventory, email and analytics, by name, and each handles order ORD-1. It works, but the order service knows three services by name, and a fourth — loyalty points — means editing it.

```
  inventory [ORD-1], email [ORD-1], analytics [ORD-1].
  the order service knows 3 services by name. a fourth, loyalty points, means editing it.
```

### Publish Once, And Redis Fans It Out

Redis is running in a container. Inventory, email and analytics each open a connection and subscribe to `orders.placed`. The order service publishes ORD-1 once, and Redis answers: 3 receivers. Each gets ORD-1.

Then loyalty points starts — not as another object, but as a second Java program with its own memory, sharing nothing with the order service except Redis's address. ORD-2 is published, Redis answers 4, and the loyalty program prints ORD-2 and exits cleanly. The order service was not changed.

```
  the order service published OrderPlaced ORD-1 once. Redis answered: 3 receivers.
  inventory [ORD-1], email [ORD-1], analytics [ORD-1]. each on a connection of its own.
  loyalty points starts as a separate Java process. ORD-2 is published: 4 receivers.
  the loyalty process printed [ORD-2] and exited with code 0. the order service was not changed.
```

### A Subscriber That Arrives Late

Only email is listening, and three orders are published: Redis answers 1, 1 and 1. Loyalty starts listening, and ORD-4 is published to 2 receivers. Email saw all four; loyalty saw only ORD-4. There is no reading from the start, because Redis stored none of the orders: the database holds 0 keys.

```
  3 orders published while only email listened. Redis answered: [1, 1, 1].
  loyalty starts listening, and ORD-4 is published: 2 receivers.
  email saw [ORD-1, ORD-2, ORD-3, ORD-4]. loyalty saw [ORD-4].
  there is no reading from the start. Redis stored none of the 4 orders: keys in the database: 0.
```

### Each Takes What It Wants

Email subscribes to the exact name `orders.placed`. Analytics subscribes to the pattern `orders.*`. A placed order reaches 2 receivers; a cancelled order reaches 1. Email heard only the placed order; analytics heard both.

```
  OrderPlaced ORD-1 reached 2 receivers. OrderCancelled ORD-1 reached 1.
  email listened to orders.placed: [OrderPlaced ORD-1].
  analytics listened to orders.*: [OrderPlaced ORD-1, OrderCancelled ORD-1].
```

### A Subscriber That Cannot Keep Up

This is the headline of the project. The demo lowers the output buffer limit from Redis's 32mb to 1mb, so the point arrives in seconds rather than minutes. Email and analytics both subscribe. Then analytics stops reading — its handler simply does not return, as a service stuck on a slow call would behave. The order service publishes a flash sale, in rounds of 1000 orders, until Redis acts.

Redis does not wait for analytics, and does not slow the publisher. The orders analytics has not read first fill the network between Redis and the demo, then pile up in Redis's buffer for analytics. When that pile passes 1mb, Redis closes analytics' connection. Its own counter of listeners cut off for falling behind reads 1, and the answer to the next publish drops from 2 receivers to 1. Email kept reading and received every order. When analytics starts reading again it gets some of the orders — whatever was already on its way through the network — and then the connection ends. Everything in the pile was thrown away with it.

How many orders it takes, and how many analytics still receives, depend on how much the network between the demo and the container holds, so the demo describes them rather than printing them. The outcome does not vary.

```
  Redis keeps a pile of unsent messages for each listener, with a limit. out of the box: 32mb, or 8mb for 60 seconds.
  this demo lowers it to 1mb. analytics stops reading, and orders are published in rounds of 1000 until Redis acts.
  more than 10,000 orders later, Redis cut analytics off. listeners cut off for falling behind: 1.
  the first order reached 2 receivers, the last reached 1. email kept up and received every one.
  analytics started reading again and got some of them, not all, then its connection ended.
  the publisher was never slowed down, and never told. the orders analytics missed are gone.
```

Why would Redis do this? The alternatives are worse. Waiting for the slow listener would let one stuck service slow down every publisher. Piling up without a limit would eventually run Redis itself out of memory, and then every listener loses. Cutting off the one that fell behind keeps everyone else going.

### The Bill

Email is down when ORD-1 is placed. Redis tells the order service: 0 receivers. When email comes back it gets nothing, because there is nothing to catch up from. The count is honest, but it is only a count of connections: not which ones, and not whether any of them finished the work. And Redis is a separate program to run and watch — this demo needed one container and two Java processes.

```
  email was down when ORD-1 was placed. Redis told the order service: 0 receivers.
  email came back and got: []. there is nothing to catch up from.
  the count says how many connections were listening. not which ones, and not whether any finished the work.
  and Redis is a separate program to run and watch: this demo needed 1 container and 2 Java processes.
```

## The verdict

Use Redis publish-and-subscribe for news that is worth nothing if it arrives late: a live price, a "someone is viewing this" count, a signal to clear a cache. Then keep three rules. Subscribe before you need it, because nothing is kept for a latecomer. Keep every listener reading — hand slow work to a queue of its own — and watch Redis's counter of listeners cut off. And if a missed order would matter, use a tool that keeps a log.

## How to recognise this in code you did not write

- A `publish` call whose return value is thrown away. Somebody could have learned that nobody was listening.
- A `subscribe` handler that does real work — a database write, an email send — directly on the listening thread. That is the listener that falls behind in a flash sale.
- A `client-output-buffer-limit` line for `pubsub` in the Redis configuration, or its absence, which means 32mb.
- Code that publishes at start-up, before its subscribers have had a chance to connect.

## Where you have already met this

Live notifications that are worthless when late, and cache invalidation signals across a fleet of servers. Redis publish-and-subscribe is common for these because Redis is often already there.

## When this is too much

If every subscriber lives in one program, a topic in memory costs nothing to run. And if a lost order matters, this is too little rather than too much: it keeps nothing and waits for nobody.
