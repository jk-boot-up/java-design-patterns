# Anti-Corruption Layer Pattern — UML Sequence Diagrams

Four sequences.

## 1. Bad Data

![Bad Data](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant F as feature
    participant A as adapter
    participant L as old system
    F->>A: stockOf("MUG-BLUE")
    A->>L: fetch
    L-->>A: quantity 12X
    A-->>F: UntranslatableLegacyData, sku named
```

</details>

## 2. A New Code

![A New Code](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant L as old system
    participant A as adapter
    L->>A: status H
    A->>A: H means ON_HOLD
    Note over A: one decision for the whole shop
```

</details>

