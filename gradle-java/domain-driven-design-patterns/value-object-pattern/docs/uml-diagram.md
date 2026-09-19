# Value Object Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Refused Mix

![A Refused Mix](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant G as GBP 10.00
    C->>G: plus(USD 10.00)
    G-->>C: CurrencyMismatch
```

</details>

## 2. A Shared Price

![A Shared Price](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as order A
    participant P as GBP 20.00
    participant B as order B
    B->>P: minus(5.00)
    P-->>B: a new GBP 15.00
    Note over A,P: order A still holds GBP 20.00
```

</details>

## 3. An Email At The Door

![An Email At The Door](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as signup
    participant E as EmailAddress
    S->>E: of("not an email")
    E-->>S: IllegalArgumentException
    Note over S: no invalid address exists anywhere
```

</details>

## 4. An Allocation

![An Allocation](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant B as billing
    participant M as Money
    B->>M: allocate(3)
    M-->>B: three shares that add up
```

</details>

