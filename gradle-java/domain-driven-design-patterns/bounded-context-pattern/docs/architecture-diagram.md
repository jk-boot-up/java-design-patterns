# Bounded Context Pattern — Architecture Diagram

Contexts do not import each other. They meet at the id and the event.

![Bounded Context Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    S["Sales context: Buyer"] -->|CustomerRenamed| B["event bus"]
    B --> H["Shipping context: Recipient"]
    B -.->|no translator yet| U["Support context: Contact"]
    S --- I["CustomerId: shared"]
    H --- I
    U --- I
```

</details>
