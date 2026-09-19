# Event-Driven Architecture Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The order service appends an order placed event to the log, and it is done. Later, shipping, which was down, comes back. It reads the log from its position, gets three events, and plans each. Inventory, which was up, read the first one long ago. Nobody called anybody.

![Event-Driven Architecture pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as order service
    participant L as log
    participant S as shipping
    O->>L: append OrderPlaced ORD-1
    Note over S: was down
    S->>L: read from my position
    L-->>S: ORD-1
    S->>S: plan delivery
```

</details>

The load-bearing sentence: **the writer never calls a reader.**
