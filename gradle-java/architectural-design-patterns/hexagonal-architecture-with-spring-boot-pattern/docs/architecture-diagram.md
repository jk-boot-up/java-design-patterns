# Hexagonal Architecture with Spring Boot Pattern — Architecture Diagram

Everything points at the core. The core points at nothing outside itself.

![Hexagonal Architecture with Spring Boot Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["ConsoleCheckout"] --> P["PlaceOrder port"]
    B["CsvBatch"] --> P
    P --> S["PlaceOrderService, the core"]
    S --> O["OrderStore port"]
    S --> W["Warehouse port"]
    S --> Y["Payments port"]
    O --> M["memory or jdbc"]
    W --> M
    Y --> N["CardNetwork"]
```

</details>
