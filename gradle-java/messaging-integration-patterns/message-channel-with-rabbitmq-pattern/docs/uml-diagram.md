# Message Channel with RabbitMQ Pattern — UML Sequence Diagrams

Four sequences. The restart comes first, because it is the one thing a channel inside one program can never show.

## 1. The Broker Restarts

Two queues, both written down, each holding the same three orders. The only difference is the flag on each message. The broker program is stopped and started again, and only the messages that were marked to be written down come back.

![The broker restarts](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant K as queue pick-orders-kept
    participant Q as queue pick-orders-quick
    participant B as broker program
    C->>K: 3 orders, each marked write to disk
    C->>Q: 3 orders, each marked memory only
    Note over K,Q: both queues are durable, both hold 3
    B-->>B: stop_app, then start_app
    B->>K: read back from disk: 3 orders
    B->>Q: queue is back, memory was not: 0 orders
```

</details>

## 2. Nobody Is Listening Yet

The warehouse is not running, so no receiver exists anywhere. Checkout sends three orders and none of them fail. The broker holds all three. When the warehouse starts, it works through them in the order they went in.

![Nobody is listening yet](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant B as queue pick-orders-waiting
    participant W as warehouse
    C->>B: ORD-1
    C->>B: ORD-2
    C->>B: ORD-3
    Note over B: no receiver exists, holding 3
    W->>B: started, ready for work
    B->>W: ORD-1, then ORD-2, then ORD-3
    W->>B: done, done, done
```

</details>

## 3. A Crash Before Saying Done

A picker takes the order and dies without a word. The broker had kept a copy, so it puts the order back and hands it to the next picker, marked as seen before.

![A crash before saying done](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant B as queue pick-orders-in-progress
    participant P1 as first picker
    participant P2 as second picker
    P1->>B: take one, not done yet
    B->>P1: ORD-1
    Note over P1: connection aborted, no goodbye
    B-->>B: waiting again: 1
    P2->>B: take one
    B->>P2: ORD-1, seen before: true
    P2->>B: done
    B-->>B: waiting: 0
```

</details>

## 4. A Channel With Room For Five

The warehouse stays down and checkout sends eight. The queue has room for five and has been told to refuse, not to drop the oldest. Checkout asked for a receipt on every send, so it hears each refusal.

![A channel with room for five](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant B as queue pick-orders-bounded
    C->>B: ORD-1 to ORD-5
    B->>C: receipt: taken, five times
    C->>B: ORD-6
    B->>C: receipt: refused
    C->>B: ORD-7 and ORD-8
    B->>C: receipt: refused, twice
    Note over C,B: 5 accepted, 3 refused, 5 waiting
```

</details>
