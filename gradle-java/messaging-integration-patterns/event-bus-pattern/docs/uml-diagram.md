# Event Bus Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Dead Event

![A Dead Event](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as poster
    participant B as bus
    participant D as DeadEvent subscriber
    O->>B: post(OrderPlaced)
    B->>B: nobody listens for OrderPlaced
    B->>D: DeadEvent(OrderPlaced)
```

</details>

