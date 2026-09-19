# Delegation Pattern — Architecture Diagram

The order does not price. Its helper does. Helpers can be chained.

![Delegation Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    O["Order.total()"] -->|hands on| R["rule: premium then gift wrap"]
    R --> P["premium"]
    R --> G["gift wrap"]
```

</details>
