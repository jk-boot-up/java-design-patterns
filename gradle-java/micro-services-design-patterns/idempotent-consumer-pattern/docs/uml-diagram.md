# Idempotent Consumer — Sequence Diagrams

Five acts, five sequences. The fourth one is rendered; the rest are here to read.

![Idempotent Consumer sequence diagram](images/uml-diagram.png)

## Act Four — One Commit Covers Both

```mermaid
sequenceDiagram
    participant B as MessageBroker
    participant C as IdempotentConsumer
    participant D as NotificationsDatabase

    B->>C: handle(msg-1)
    C->>D: hasHandled(msg-1)?
    D-->>C: no
    C->>D: begin()
    C->>D: queueConfirmation(text)
    C->>D: recordHandled(msg-1)
    C->>D: commit()
    D-->>C: both rows, or neither
    Note over B,C: the acknowledgement is lost
    B->>C: handle(msg-1) again
    C->>D: hasHandled(msg-1)?
    D-->>C: yes
    C--)B: ignored, nothing written
```

The second delivery is a read and nothing else. `ignoringIsCheap` is the test that says so.

## Act One — A Set Of Ids, And It Works

```mermaid
sequenceDiagram
    participant B as MessageBroker
    participant C as NaiveConsumer
    participant D as NotificationsDatabase

    B->>C: handle(msg-1)
    C->>D: queueConfirmationOnItsOwn(text)
    C->>C: seen.add(msg-1)
    Note over B,C: the acknowledgement is lost
    B->>C: handle(msg-1) again
    C->>C: seen.contains(msg-1)? yes
    C--)B: skipped
```

Correct about what to do, wrong about where to keep the evidence.

## Act Two — The Deploy

```mermaid
sequenceDiagram
    participant B as MessageBroker
    participant C as NaiveConsumer
    participant D as NotificationsDatabase

    B->>C: handle(msg-1)
    C->>D: queueConfirmationOnItsOwn(text)
    C->>C: seen.add(msg-1)
    Note over C: restart - the set is empty again
    B->>C: handle(msg-1) again
    C->>C: seen.contains(msg-1)? no
    C->>D: queueConfirmationOnItsOwn(text)
    Note over D: two confirmations for one order
```

The database survived the deploy and the set did not.

## Act Three — The Gap

```mermaid
sequenceDiagram
    participant B as MessageBroker
    participant C as NaiveConsumer
    participant D as NotificationsDatabase

    B->>C: handle(msg-1)
    C->>D: queueConfirmationOnItsOwn(text)
    Note over C: dies here, before remembering the id
    Note over C: restart
    B->>C: handle(msg-1) again
    C->>D: queueConfirmationOnItsOwn(text)
```

No restart is needed to cause this, only a crash in the wrong instant. Two writes, two
moments, one gap.

## Act Five — The Handler That Needed None Of It

```mermaid
sequenceDiagram
    participant B as MessageBroker
    participant S as ShipmentStatusConsumer

    B->>S: handle(ShipmentDispatched)
    S->>S: status[ord-7006] = SHIPPED
    B->>S: handle(ShipmentDispatched) again
    S->>S: status[ord-7006] = SHIPPED
    Note over S: same status, no store, no transaction
```

There is no database in this diagram at all, and that is the point of it.

## Notes On Reading These

**Dashed arrows are things that did not happen.** An ignored redelivery writes nothing.

**The duplicate is never prevented, only absorbed.** In every diagram the broker delivers
twice. Nothing on the receiving side can stop that; the only question is what the second
delivery does.

**The exactly-once lives in one box.** Not in the broker, not in the network — in the
`commit()` inside `NotificationsDatabase`.

**The timings are exact.** `SimulatedClock` advances by fixed amounts — ten milliseconds for
a delivery, five for a commit — so the timelines in the demo output match these sequences
step for step on any machine.
