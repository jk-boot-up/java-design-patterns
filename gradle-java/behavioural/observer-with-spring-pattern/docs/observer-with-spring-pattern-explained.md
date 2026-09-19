# Observer with Spring, Explained

## The pattern in one sentence

In Spring, an observer is a method marked as an event listener. The publisher only knows the event.

## What is new here

The pattern is [Observer](../observer-pattern). This page is only what Spring Boot adds.

### The Subject Knows Nobody

The order publishes one event. Four listeners react, in order, and the order holds only a publisher.

```
  inventory: released stock for ORD-000001 on main
  email: told the customer about ORD-000001
  analytics: counted ORD-000001 as SHIPPED
  warehouse feed: pick line for ORD-000001
```

### On The Caller's Thread

By default the listeners run on the thread that published the event, before the publish call returns.

```
  the caller is main, and every listener above ran on it.
```

### One Listener Fails

When the email listener throws, the exception reaches the caller and the listeners after it are skipped. The order was already shipped.

```
  the caller got: mail server timed out.
  order shipped: true.
  inventory: released stock for ORD-000002 on main
  analytics and the warehouse feed never heard about ORD-000002.
```

### A Listener On Another Thread

Mark a listener asynchronous and it runs on another thread, after the publish call may already have returned.

```
  cancel() has returned. journal so far: [inventory: released stock for ORD-000003 on main, email: told the customer about ORD-000003, analytics: counted ORD-000003 as CANCELLED].
  after the gate opened: 1 audit line, on a thread named task-1.
```

### A Listener That Filters

A condition on the annotation selects which events a listener wants.

```
  shipped: the warehouse feed heard: true.
  cancelled: the warehouse feed heard: false.
```

### An Event Nobody Hears

An event with no listener is dropped without error.

```
  refund published. listeners that ran: 0. errors: 0.
  a publisher cannot tell whether anyone is listening.
```

## The verdict

Publish events, keep listeners independent, and give each listener the thread it needs. Catch failures inside a listener that must not stop the others. Test that the listener is actually there.

## How to recognise this in code you did not write

- `ApplicationEventPublisher` in a constructor.
- `@EventListener` or `@TransactionalEventListener` on a method.
- A method whose only argument is a record named like a past-tense event.

## Where you have already met this

Every Spring application that reacts to something: startup, a context refresh, or your own domain events.

## When this is too much

When there is one reaction and it must succeed, call it directly. An event is for reactions that may come and go.
