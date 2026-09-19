# Event Bus, Explained

## The pattern in one sentence

An event bus is a single place where components post events and subscribe to the kinds they care about, so that none of them holds a reference to any other.

## The six acts

### Everyone Knows Everyone

Five components that each tell each other about orders need twenty references between them. A sixth needs ten more.

```
  5 components that each tell each other about orders: 20 references between them.
  add a sixth and it needs 10 more.
```

### Everyone Knows The Bus

One post reaches inventory, email and analytics. Five components each hold one reference, to the bus: five references, not twenty. The poster holds no reference to any subscriber.

```
  [inventory saw ORD-1, email saw ORD-1, analytics saw ORD-1].
  5 components, each with 1 reference to the bus: 5 references, not 20. the poster has no reference to any subscriber.
```

### By Type

A subscriber for order placed hears only that. A subscriber for every order event hears both the placed and the cancelled.

```
  a subscriber for OrderPlaced heard: [ORD-1].
  a subscriber for every OrderEvent heard: [OrderPlaced ORD-1, OrderCancelled ORD-1].
```

### One Failing Subscriber

Email fails, and analytics still hears the event. The failure is recorded. The poster does not see it: it posted, and carried on.

```
  email failed, analytics still heard it: [analytics counted ORD-1]. recorded: [OrderPlaced: mail server timed out].
  the poster did not see the failure. it posted, and carried on.
```

### An Event Nobody Hears

With no subscriber, an event is counted as dead, and nothing complains. With a subscriber for dead events, the unheard event arrives there.

```
  no subscriber yet. dead events counted: 1, and nothing complained.
  with a subscriber for DeadEvent: [OrderPlaced[orderId=ORD-2, pence=100]].
  a typo in an event type, or a forgotten subscription, is a silent loss unless something listens for dead events.
```

### The Bill

Nothing in the code that posts an event says who reacts to it, though the bus can be asked. A thousand short-lived subscribers that never cancel are all still held. Cancelling leaves none. And a slow subscriber holds up the poster.

```
  who reacts to an OrderPlaced? nothing in the code that posts it says. the bus can be asked: 2 subscribers.
  1000 short-lived components subscribe and are then thrown away without unsubscribing: 1002 subscribers still held.
  the same, each cancelling its subscription: 0 held.
  and delivery is a plain method call in one process: a slow subscriber holds up the poster.
```

## The verdict

Use an event bus inside a program to decouple components that react to what happened. Type the events, subscribe by type, always cancel a subscription when the subscriber goes away, listen for dead events, and keep a list of who reacts to what somewhere a person can find. Do not use one across processes, where you need a real broker, or where the poster needs an answer.

## How to recognise this in code you did not write

- `eventBus.post(...)` and `@Subscribe` in Guava.
- Spring's `ApplicationEventPublisher` and `@EventListener`.
- Android's `LocalBroadcastManager`, and Vert.x's `EventBus`.
- Classes with names ending in `Listener` or `Subscriber` and no visible caller.

## Where you have already met this

Guava's `EventBus`, Spring's application events, GreenRobot's EventBus, and every UI toolkit's event system.

## When this is too much

For two components that always talk, a direct call is clearer. A bus is for many-to-many, and its cost is a flow you cannot see by reading one class.
