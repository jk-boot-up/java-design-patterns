# Pipes and Filters Pattern — Architecture Diagram

Each line goes through every filter, in order.

![Pipes and Filters Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    L["order lines"] --> P["parse"]
    P --> V["validate"]
    V --> R["price"]
    R --> T["tax"]
    T --> F["format"]
    F --> O["confirmations"]
    P -.->|dropped, with a reason| X["rejects"]
    V -.-> X
```

</details>
