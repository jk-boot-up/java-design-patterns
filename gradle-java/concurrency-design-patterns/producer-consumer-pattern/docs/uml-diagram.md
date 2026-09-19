# Producer–Consumer Pattern — UML Sequence Diagrams

Four sequences: the queue at capacity, a clean shutdown, an abrupt one, and
the lost-update race the shared harness is proven against.

## 1. The Queue Reaches Capacity, And Says No

![Producer-Consumer pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Main as Test thread
    participant Q as BoundedOrderQueue «capacity 3»
    participant Packer as packer thread

    Main->>Q: put(ord-holding)
    Packer->>Q: take() -> ord-holding
    Packer->>Packer: pack(ord-holding) — parked at a Gate
    Note over Main: CountDownLatch confirms the packer<br/>has taken ord-holding and is now parked
    Main->>Q: put(ord-1), put(ord-2), put(ord-3)
    Note over Q: size() == 3 == capacity, guaranteed
    Main->>Q: offer(ord-overflow, 150ms)
    Q-->>Main: false — rejected, no room in time
```

</details>

## 2. Clean Shutdown — The Pill Travels Through The Queue

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Main as Test thread
    participant Q as BoundedOrderQueue
    participant Packer as packer thread

    Main->>Q: put(ord-1..4)
    Main->>Q: put(POISON)
    loop 4 times
        Packer->>Q: take()
        Q-->>Packer: ord-N
        Packer->>Packer: pack ord-N, then log it
    end
    Packer->>Q: take()
    Q-->>Packer: POISON
    Note over Packer: sees POISON, returns — thread exits cleanly
```

</details>

## 3. Abrupt Shutdown — Whatever Is Queued Is Lost

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Main as Test thread
    participant Q as BoundedOrderQueue
    participant Packer as packer thread

    Main->>Q: put(ord-holding)
    Packer->>Q: take() -> ord-holding
    Packer->>Packer: pack(ord-holding) — parked at a Gate
    Note over Main: latch confirms the packer is parked
    Main->>Q: put(ord-1), put(ord-2), put(ord-3)
    Main->>Packer: interrupt()
    Note over Packer: Gate converts the interrupt into a signal,<br/>pack returns, isInterrupted is true,<br/>ord-holding is NOT logged as packed
    Packer-->>Main: thread exits
    Note over Q: ord-1, ord-2, ord-3 still queued — never taken
```

</details>

## 4. The Harness's Own Proof — A Lost Update, Every Run

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T1 as Thread 1
    participant T2 as Thread 2
    participant R as Rendezvous «2 parties»
    participant S as shared int, starts at 10

    T1->>S: read -> 10
    T2->>S: read -> 10
    T1->>R: meet()
    T2->>R: meet()
    Note over R: both released together, only once both have arrived
    T1->>S: write 10 - 1 = 9
    T2->>S: write 10 - 1 = 9
    Note over S: final value: 9, not 8 — one decrement is lost, every run
```

</details>

This is the mechanism reused, with different shared state, in
Read–Write Lock and Monitor Object later in this category.
