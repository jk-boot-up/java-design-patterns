# Singleton with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. One Bean Shared

![One Bean Shared](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as Checkout
    participant M as AdminConsole
    participant G as generator
    K->>G: nextOrderNumber
    G-->>K: ORD-000001
    M->>G: nextOrderNumber
    G-->>M: ORD-000002
```

</details>

## 2. A Scope Change

![A Scope Change](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as Checkout
    participant M as AdminConsole
    K->>K: its own generator: ORD-000001
    M->>M: its own generator: ORD-000001
```

</details>

## 3. A Forced Duplicate

![A Forced Duplicate](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T1 as customer 1
    participant F as plain long
    participant T2 as customer 2
    T1->>F: read 0
    T2->>F: read 0, write 1
    T1->>F: write 1
```

</details>

