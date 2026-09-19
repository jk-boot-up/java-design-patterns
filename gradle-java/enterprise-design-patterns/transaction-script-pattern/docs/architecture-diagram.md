# Transaction Script Pattern — Architecture Diagram

A request runs one script, in one transaction.

![Transaction Script Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    R["request: place an order"] --> S["PlaceOrderScript"]
    S --> T["one transaction"]
    T --> D["Db: stock, orders"]
    S --> P["Payment"]
```

</details>
