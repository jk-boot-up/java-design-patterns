# Identity Map Pattern — UML Sequence Diagrams

Four sequences.

## 1. Two Loads, Two Objects

![Two Loads, Two Objects](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant P as PlainCustomerMapper
    participant DB as database
    Caller->>P: find(7)
    P->>DB: select
    P-->>Caller: object A
    Caller->>P: find(7)
    P->>DB: select
    P-->>Caller: object B, not A
```

</details>

## 2. The Lost Change

![The Lost Change](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as object A
    participant B as object B
    participant DB as database
    A->>A: moveTo York
    B->>B: changeEmail
    A->>DB: save whole row, York
    B->>DB: save whole row, old address
    Note over DB: York is gone
```

</details>

## 3. One Map, One Object

![One Map, One Object](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant S as CustomerSession
    participant M as identity map
    Caller->>S: find(7)
    S->>M: miss, load and put
    Caller->>S: find(7)
    S->>M: hit
    S-->>Caller: the same object
```

</details>

## 4. A Stale Session

![A Stale Session](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as session
    participant DB as database
    participant O as other process
    S->>DB: load customer 7
    O->>DB: change the email
    S->>S: find(7), from the map
    Note over S: still the old email
```

</details>

