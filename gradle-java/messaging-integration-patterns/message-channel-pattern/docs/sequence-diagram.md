# Message Channel Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Checkout places an order and sends a pick order message to the channel, and carries on straight away. The warehouse is down, so nothing takes the message, and it waits. Later the warehouse comes back and asks the channel for a message, and takes the pick order. It picks the order. Checkout was never held up.

![Message Channel pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant Q as channel
    participant W as warehouse
    C->>Q: send(PickOrder ORD-1)
    Q-->>C: accepted
    Note over W: down
    W->>Q: receive, once it is back
    Q-->>W: PickOrder ORD-1
    W->>W: pick the order
```

</details>

The load-bearing sentence: **the sender is not held up by the receiver.**
