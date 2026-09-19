# Identity Map with JPA Pattern — UML Sequence Diagrams

Four sequences.

## 1. Two Finds, One Context

![Two Finds, One Context](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant EM as EntityManager
    participant DB as H2
    Caller->>EM: find(Customer, 7)
    EM->>DB: select
    Caller->>EM: find(Customer, 7)
    Note over EM: from the context, no SQL
```

</details>

## 2. Two Changes, One Update

![Two Changes, One Update](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant EM as EntityManager
    participant DB as H2
    Caller->>EM: customer.moveTo(York)
    Caller->>EM: customer.changeEmail(new)
    Caller->>EM: commit
    EM->>DB: one UPDATE with both changes
```

</details>

## 3. Two Contexts

![Two Contexts](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant EM1 as context one
    participant EM2 as context two
    participant DB as H2
    EM1->>DB: select customer 7
    EM2->>DB: select customer 7
    Note over EM1,EM2: two objects, not ==
```

</details>

## 4. A Detached Change

![A Detached Change](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant EM as context
    participant C as customer
    participant DB as H2
    EM->>C: loaded
    EM->>EM: close, customer is detached
    C->>C: moveTo(Nowhere)
    Note over C,DB: nothing tracks it, nothing is saved
```

</details>

