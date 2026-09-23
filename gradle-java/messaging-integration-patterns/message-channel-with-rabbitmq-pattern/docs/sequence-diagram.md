# Message Channel with RabbitMQ Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Checkout sends one pick order, for order number one, to the broker, and goes straight back to selling; nobody is listening yet. The broker puts the order in a queue and holds it. Some time later a picker in the warehouse starts up and asks for work. The broker hands the order over, but keeps its own copy. The picker crashes before it says it is done. The broker notices the connection has gone, and puts the order back in the queue, marked as seen before. A second picker starts and asks for work. The broker hands it the same order, with the mark on it. This picker picks it and says done. Only now does the broker forget the order. Two deliveries, one order picked, nothing left waiting.

![Message Channel with RabbitMQ sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant B as RabbitMQ queue
    participant P1 as first picker
    participant P2 as second picker
    C->>B: send ORD-1, then carry on selling
    Note over B: nobody is listening, the broker holds it
    P1->>B: ready for work
    B->>P1: ORD-1, the broker keeps a copy
    Note over P1: crashes before saying done
    B-->>B: connection gone, put ORD-1 back, marked as seen before
    P2->>B: ready for work
    B->>P2: ORD-1, seen before: true
    P2->>B: done
    B-->>B: forget ORD-1. deliveries 2, picked 1, waiting 0
```

</details>

The load-bearing sentence: **a broker forgets a message only when the receiver says it is done, so a crash costs a second delivery, never a lost order.**

For the restart, the full channel and the rest of the failure modes, see [`uml-diagram.md`](uml-diagram.md).
