# Specification Pattern — UML Sequence Diagrams

Four sequences.

## 1. Building A Rule

![Building A Rule](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant B as Products
    B->>B: inStock()
    B->>B: priceUnder(1000)
    B->>B: inStock().and(priceUnder).and(discontinued().not())
    B-->>B: one rule
```

</details>

## 2. Selecting

![Selecting](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as Catalogue
    participant R as rule
    C->>R: isSatisfiedBy(product 1)
    C->>R: isSatisfiedBy(product 2)
    Note over C,R: every product is asked
```

</details>

