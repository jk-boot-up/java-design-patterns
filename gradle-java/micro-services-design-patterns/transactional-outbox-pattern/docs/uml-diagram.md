# Transactional Outbox — Sequence Diagrams

Five acts, five sequences. The third one is rendered; the rest are here to read.

![Transactional Outbox sequence diagram](images/uml-diagram.png)

## Act Three — One Commit, Then A Sweep

```mermaid
sequenceDiagram
    participant C as Checkout
    participant O as OrderService
    participant D as OrderDatabase
    participant R as OutboxRelay
    participant B as MessageBroker
    participant N as NotificationService

    C->>O: placeOrder(order)
    O->>D: begin()
    O->>D: save(order)
    O->>D: save(outbox message)
    O->>D: commit()
    D-->>O: both rows, or neither
    Note over O,B: OrderService never calls the broker
    R->>D: unsent()
    D-->>R: msg-1
    R->>B: publish(msg-1)
    B->>N: deliver
    B-->>R: accepted
    R->>D: markSent(msg-1)
```

The top half is the checkout and it ends at the commit. The bottom half happens later, in a
different process, and the customer is long gone by then.

## Act Two — The Naive Version, And The Gap

```mermaid
sequenceDiagram
    participant C as Checkout
    participant O as NaiveOrderService
    participant D as OrderDatabase
    participant B as MessageBroker

    C->>O: placeOrder(order)
    O->>D: saveOnItsOwn(order)
    D-->>O: committed
    Note over O: the process dies here
    O--)B: publish never happens
    Note over O,B: the order is real and nothing knows a message was owed
```

There is no second half to this diagram, and that is the whole comparison.

## Act Four — The Broker Is Down

```mermaid
sequenceDiagram
    participant R as OutboxRelay
    participant D as OrderDatabase
    participant B as MessageBroker

    R->>D: unsent()
    D-->>R: msg-1, msg-2
    R->>B: publish(msg-1)
    B--)R: no answer
    Note over R,D: left in the tray, nothing is marked sent
    R->>B: publish(msg-2)
    B--)R: no answer
    Note over R: second sweep, later
    R->>B: publish(msg-1)
    B-->>R: accepted
    R->>D: markSent(msg-1)
    R->>B: publish(msg-2)
    B-->>R: accepted
    R->>D: markSent(msg-2)
```

Nothing in this diagram is retry logic. The second sweep reads the same unsent rows because
nobody marked them sent.

## Act Five — The Duplicate

```mermaid
sequenceDiagram
    participant R as OutboxRelay
    participant B as MessageBroker
    participant N as NotificationService
    participant D as OrderDatabase

    R->>B: publish(msg-1)
    B->>N: deliver - email 1
    B-->>R: accepted
    Note over R,D: the relay dies before markSent
    Note over R: restart, and the tray still holds msg-1
    R->>B: publish(msg-1)
    B->>N: deliver - email 2
    B-->>R: accepted
    R->>D: markSent(msg-1)
```

Two emails, one order, and the same message id on both. That id is the only thing the
receiving side has to work with, and it is enough.

## Act One — For Completeness

```mermaid
sequenceDiagram
    participant O as NaiveOrderService
    participant D as OrderDatabase
    participant B as MessageBroker
    participant N as NotificationService

    O->>D: saveOnItsOwn(order)
    D-->>O: committed
    O->>B: publish(msg)
    B->>N: deliver
    B-->>O: accepted
```

The happy path, which is what every test written for the naive version will see.

## Notes On Reading These

**Dashed arrows are failures or things that never happened.** Solid ones completed.

**Nothing here is a distributed transaction.** No participant holds a lock while waiting for
another. The only transaction anywhere is an ordinary database one, and it covers two rows
in the same database.

**The two halves of act three run at different times, and possibly for different reasons.**
The checkout half runs because a customer pressed a button. The relay half runs because a
timer fired. They share nothing but a table.

**The timings are exact.** `SimulatedClock` advances by fixed amounts — fifteen milliseconds
for a broker publish, seven for a notification — so the timelines in the demo output match
these sequences step for step on any machine.
