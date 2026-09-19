# Event-Driven Architecture with Kafka Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The order service sends an order placed event to Kafka, and Kafka replies with offset three. That is all the order service does. Shipping, which was down, starts, and asks Kafka where its group left off. Kafka says offset one. Shipping reads offsets one to three, plans each, and commits offset four. Nobody called anybody.

![Event-Driven Architecture with Kafka pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as order service
    participant K as Kafka
    participant S as shipping
    O->>K: send OrderPlaced ORD-4
    K-->>O: offset 3
    Note over S: was down
    S->>K: where did my group stop?
    K-->>S: offset 1
    S->>K: read from offset 1
    K-->>S: ORD-2, ORD-3, ORD-4
    S->>K: commit offset 4
```

</details>

The load-bearing sentence: **the writer never calls a reader, and the broker remembers each group.**
