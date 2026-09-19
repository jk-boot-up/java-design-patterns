# Interpreter with SpEL Pattern — UML Sequence Diagrams

Four sequences.

## 1. Parse Once

![Parse Once](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant B as PromotionBook
    participant P as parser
    B->>P: four rule texts
    P-->>B: four trees
    Note over B: kept for every later order
```

</details>

## 2. A Refused Static Call

![A Refused Static Call](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant B as PromotionBook
    participant C as read-only context
    B->>C: T(java.lang.System).getProperty(...)
    C-->>B: SpelEvaluationException
```

</details>

