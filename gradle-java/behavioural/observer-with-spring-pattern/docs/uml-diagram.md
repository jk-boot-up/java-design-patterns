# Observer with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Shipment

![A Shipment](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as OrderService
    participant P as publisher
    participant L as four listeners
    O->>P: publishEvent(OrderStatusChanged)
    P->>L: in @Order, on the caller's thread
```

</details>

## 2. An Async Listener

![An Async Listener](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant P as publisher
    participant A as audit on task-1
    C->>P: publishEvent
    P->>A: hand to the executor
    P-->>C: returns at once
    A->>A: runs later
```

</details>

