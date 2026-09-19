# Transaction Script Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Successful Order

![A Successful Order](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as script
    participant D as Db
    S->>D: stockOf, setStock
    S->>D: save(order)
    D-->>S: committed
```

</details>

## 2. Two Scripts, One Rule

![Two Scripts, One Rule](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as PlaceOrderScript
    participant A as AmendOrderScript
    participant H as Pricing
    P->>H: total(sku, quantity)
    A->>H: total(sku, quantity)
    Note over H: the rule lives once
```

</details>

