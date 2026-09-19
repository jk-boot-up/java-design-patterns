# Service Layer Pattern — UML Sequence Diagrams

Four sequences.

## 1. Two Doors, Two Copies

![Two Doors, Two Copies](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant W as web
    participant C as CLI copy
    participant P as payment
    W->>W: reserve stock, then charge
    C->>P: charge first
    C->>C: reserve stock, refused
    Note over C,P: charged, no order
```

</details>

## 2. Everything In The Order

![Everything In The Order](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as Order.place
    participant G as gateway
    participant E as email
    participant DB as database
    O->>G: charge
    O->>DB: write
    O->>E: send
    Note over O: six collaborators
```

</details>

## 3. One Service

![One Service](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Web
    participant Cli
    participant S as OrderService
    Web->>S: placeOrder
    Cli->>S: placeOrder
    Note over S: the same steps for both
```

</details>

## 4. A Refused Order

![A Refused Order](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as OrderService
    participant DB as database
    participant D as Product
    S->>DB: begin
    S->>D: reserve 5 mice
    D-->>S: refused, only 3
    S->>DB: rollback
    Note over S: nothing charged, nothing emailed
```

</details>

