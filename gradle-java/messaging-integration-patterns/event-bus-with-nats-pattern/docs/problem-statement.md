# Problem Statement

## Read the partner first

This project assumes [Event Bus](../../event-bus-pattern), which showed one meeting place inside a single program: components posting events without holding a reference to anybody, subscribers picking events by what they are, one subscriber failing without taking the others with it, and an event nobody heard turned into a dead event. Nothing here is lost by skipping NATS, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The same online store. Checkout publishes what happened: an order was placed, an order was cancelled, a payment was taken, stock is running low. The email service, the warehouse and the analytics tally each listen for what they care about. Nobody holds a reference to anybody.

The difference is that these are now separate programs on a network, and the meeting place is a separate program too.

## What is new

**NATS**, a real message bus in a container. It is a tannoy in a warehouse. Somebody announces that order ORD-1 has been placed, and everybody in the room at that moment hears it. Anybody who steps into the room a second later hears nothing, and there is no recording.

```
  nobody was listening. checkout published OrderPlaced ORD-1 and the bus dropped it: no error, no record, and nowhere to read it back from.
  the warehouse then started listening, and checkout published OrderPlaced ORD-2.
  the first event the warehouse ever received was OrderPlaced ORD-2. this bus delivers a name in order, so ORD-1 was never coming.
```

## The failure this project exists to show

Publishing always succeeds, and success means nothing. A subscriber that is starting up, restarting, or simply not there yet does not get a late copy, an error or a warning. The order is gone, and the only party who could have told anybody is the server, which is already busy forgetting it.

The pattern's answer is not to make the bus remember. It is to know which bus you are holding: use this one for announcements that can be missed, and ask rather than tell when an answer actually matters.
