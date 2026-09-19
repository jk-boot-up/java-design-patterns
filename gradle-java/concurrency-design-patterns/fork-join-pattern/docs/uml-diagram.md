# Fork-Join Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Leaf

![A Leaf](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as task with 10000 totals
    T->>T: small enough: add them in a loop
    T-->>T: return the sum
```

</details>

