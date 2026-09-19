# Domain Event, Explained

## The pattern in one sentence

A domain event is an immutable record of something that has already happened in the business, named in the past tense, so other parts of the system can react without the thing that raised it knowing who they are.

## The six acts

### The Order Calls Everyone

The order code saves the order, reserves stock, then sends the email, which fails. The order is saved and stock is reserved, but the caller is told it failed and analytics never counts it.

```
  the mail server is down. the caller gets: mail server timed out.
  order saved: true. what happened: [stock: reserved for ORD-1].
  saved and reserved, the customer told they failed, analytics never counted it.
```

### The Order Says What Happened

Placing the order records one event, order placed, with the id, the customer and the total. Asking again returns nothing, because the events were handed over.

```
  events recorded by place(): [OrderPlaced[orderId=ORD-2, customerId=ada, totalPence=4999]].
  the order called nobody. asked again: [].
```

### Delivered After The Save

Saving the order keeps its event. Nothing reacts yet. A relay then delivers the event to stock, email and analytics.

```
  saved. events waiting: 1. reactions so far: 0.
  stock: reserved for ORD-3
  email: confirmed ORD-3 to ada
  analytics: counted ORD-3 for 4999 pence
  events waiting now: 0.
```

### A Failing Reaction

With the mail server down, only the email reaction fails. Stock and analytics run. The event stays waiting for email alone, and when the server is back the next relay sends just that one.

```
  the mail server is down. failures: [email failed on OrderPlaced for ORD-4: mail server timed out].
  the others still ran: [stock: reserved for ORD-4, analytics: counted ORD-4 for 4999 pence].
  events still waiting: 1.
  the mail server is back. a second relay: [] failures, waiting: 0.
  the email went out once: 1, and stock was not reserved twice: 1.
```

### Events Are Facts

Placing and then cancelling records two events, in that order. Each is a record with the data in it, and no reference to the order.

```
  place then cancel: [OrderPlaced, OrderCancelled], in that order.
  each event is a record: it carries the order id and the data, not the order.
  a handler that receives one cannot reach back and change the order.
```

### The Gap Between Saving And Telling

If the process stops after the save and before the relay, nothing has reacted, but the event was saved with the order. After a restart the relay delivers it, and nothing is lost.

```
  the process stops after the save and before the relay. reactions: 0. events kept: 1.
  after a restart the relay runs. reactions: 3. nothing was lost, because the events were saved with the order.
  publishing straight after the save, with no outbox, would have lost all three.
```

## The verdict

Raise a domain event when something happens that other parts of the business care about, name it in the past tense, and keep it small. Save the events with the aggregate. Deliver them separately, expect a delivery to be repeated, and make each handler safe to run twice. Do not use events where one caller needs the answer straight away.

## How to recognise this in code you did not write

- A method that records an event instead of calling a service.
- Event classes named in the past tense: `OrderPlaced`, `PaymentReceived`.
- A list of events on an entity, collected when it is saved.
- `ApplicationEventPublisher`, `@DomainEvents` and `@TransactionalEventListener` in Spring.

## Where you have already met this

`ApplicationEvent` in Spring, `@DomainEvents` in Spring Data, and every place a system says something happened and let others decide what to do.

## When this is too much

When there is one reaction and the caller needs its answer, a plain call is clearer. An event is for reactions that may come and go, and may happen later.
