# Event Bus with NATS, Explained

## The pattern in one sentence

An event bus is one meeting place: publish to it, subscribe to it, and never hold a reference to the other side. With NATS the meeting place is a server on the network, and it keeps nothing.

## The analogy

Think of a tannoy in a warehouse. Somebody picks up the microphone and announces that order ORD-1 is ready to pack. Everybody standing in the warehouse at that moment hears it. The person on the microphone does not know who is in the room, does not wait for anybody, and is never told whether anybody acted on it. And somebody who walks into the warehouse a second later hears nothing at all. There is no recording.

That is NATS, exactly. It is not a shortcoming to be worked around. It is the deal.

## What is new here

The pattern is [Event Bus](../../event-bus-pattern). This page is only what NATS adds.

### Everyone Knows Everyone

Before there is a bus, every service tells every other service directly. Five services need twenty wires between them, because each pair needs one in each direction. Every one of those wires is a network address that some service has to be told about, and that can be wrong or point at something that is not running. Add a sixth service and it needs ten more.

```
  5 services that each tell the other four when an order is placed: 20 wires between them, and every wire is an address that can be wrong or down.
  add a sixth service and it needs 10 more.
```

### Everyone Knows The Bus

Checkout publishes an order-placed event under the name `store.orders.placed` and returns. It is told nothing about who was listening. The email service, the warehouse and the analytics tally each have their own connection, and each sees the order. Five services, one connection each: five wires, not twenty.

```
  checkout published OrderPlaced ORD-1 under the name store.orders.placed and returned. it was told nothing about who was listening.
  [email saw OrderPlaced ORD-1, warehouse saw OrderPlaced ORD-1, analytics saw OrderPlaced ORD-1].
  5 services, each with 1 connection to the bus: 5 wires, not 20.
```

### By Name

The hand-built bus let a subscriber ask for a type of event. NATS has no types; it has names, written in dotted parts. A listener can ask for one exact name, or for a family. A star stands for one part of the name, and an arrow stands for the whole rest of it.

Checkout publishes four events: an order placed, that order cancelled, a payment taken, and stock running low. A listener for `store.orders.placed` receives one. A listener for `store.orders.*` receives two, the placed and the cancelled. A listener for `store.>` receives all four.

```
  a listener for store.orders.placed received 1: [OrderPlaced ORD-1].
  a listener for store.orders.*, where the star stands for one word, received 2: [OrderPlaced ORD-1, OrderCancelled ORD-1].
  a listener for store.>, where the arrow stands for the rest of the name, received 4: [OrderPlaced ORD-1, OrderCancelled ORD-1, PaymentTaken ORD-1, StockLow SKU-42].
```

### One Failing Subscriber

The email service's handler throws: the mail server timed out. The warehouse, on a connection of its own, still reserves the stock. Checkout is never told. In the hand-built version that isolation had to be written; here it is free, because the two subscribers are not even in the same program, and because publishing had already returned before either of them ran.

```
  email's handler threw. recorded: [OrderPlaced ORD-1: mail server timed out].
  the warehouse, on a connection of its own, still reacted: [warehouse reserved ORD-1].
  checkout was never told. publishing had already returned before either of them ran.
```

### An Event Nobody Hears

This is the act the project exists for.

Nobody is listening. Checkout publishes an order-placed event for ORD-1. The call returns without error, and the bus drops it. There is no error, no record, and nowhere to read it back from. The hand-built bus noticed this and turned the event into a dead event that something could watch for. NATS has no such hook.

Then the warehouse starts listening, and checkout publishes ORD-2. The first event the warehouse ever receives is ORD-2. That is how we know ORD-1 was missed, and it is worth pausing on: nobody can prove a negative by waiting. NATS delivers one name in the order it was published, so once the second order has arrived, the first one cannot still be on its way. It was never coming.

Telling this bus is never confirmed. Asking is. A request sent under a name nobody is listening to comes back immediately, and the server says there are no responders. That is the only moment on this bus where a publisher learns that its words went nowhere.

```
  nobody was listening. checkout published OrderPlaced ORD-1 and the bus dropped it: no error, no record, and nowhere to read it back from.
  the first event the warehouse ever received was OrderPlaced ORD-2. this bus delivers a name in order, so ORD-1 was never coming.
  2 orders published, 1 received.
  telling this bus is never confirmed. asking is: a request on store.orders.cancelled with nobody listening came back at once with no responders.
```

### The Bill

Who reacts to an order being placed? Nothing in checkout says, and checkout cannot find out. The hand-built bus was an object you could ask. This one is a separate program, and only it knows. It has to be asked on a second port that exists for that, and it reports three listeners for store events.

Then analytics stops listening while keeping its connection open: two. Then all three services close their connections: none. A connection closing takes every listener on it at once, which is a real difference from the hand-built version, where every subscription had to be cancelled by hand.

And the bus is now a program of its own to run and to watch: this demo needed one container. And it keeps nothing, so a subscriber that is down when an event is published has missed it for good.

```
  who reacts to an order being placed? nothing in checkout says, and checkout cannot find out. only the server knows, and it has to be asked on a second port: 3 listeners for store events.
  analytics stopped listening but left its connection open: 2 listeners.
  after the three services closed their connections: 0 listeners. a connection closing takes every listener on it with it.
  and the bus is now a program of its own to run and to watch: this demo needed 1 container.
  and it keeps nothing. a subscriber that is down when an event is published has missed it for good.
```

## The other trade, next door

[Event-Driven Architecture with Kafka](../../../architectural-design-patterns/event-driven-architecture-with-kafka-pattern) runs a broker that keeps a durable log. A service that was down comes back and reads everything it missed; a brand new service can be built from history. The price is that the broker stores the events, tracks every reader, and may deliver the same event twice, so every reader has to be safe to repeat.

NATS makes the opposite choice on every one of those. Neither is right in general. Pick the one that matches what a missed event would cost you.

## The verdict

Use this kind of bus for announcements: cache invalidations, presence, live dashboards, telemetry, anything where the next event makes the last one irrelevant. Name your subjects for facts in the past tense, and agree the naming as a team, because the names are the contract. Always wait for the server to confirm a subscription before publishing something you want that subscriber to hear. And when an event genuinely must not be lost, do not reach for a bigger timeout: reach for a durable log, or ask instead of telling.

## How to recognise this in code you did not write

- A `Connection` from `io.nats.client`, with `publish` and `subscribe` taking a dotted string.
- Subject names with a star or an arrow in them.
- A `Dispatcher`, which is a subscription with a handler attached rather than a loop.
- A `flush` call before a publish, which is somebody who has already been bitten by the race.
- A request that fails with "no responders" rather than a timeout.

## Where you have already met this

NATS in service meshes and control planes, Redis Pub/Sub, MQTT at quality of service zero, and a browser's WebSocket fan-out. All of them make the same trade: fast, small and forgetful.

## When this is too much

For components inside one program, the hand-built [Event Bus](../../event-bus-pattern) is clearer and needs nothing installed. Reach for a server only when the parties are separate programs. And if losing an event costs a customer money, this is the wrong bus.
