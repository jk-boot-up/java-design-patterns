# Strangler Fig Pattern — UML Sequence Diagrams

Four sequences.

## 1. The Big Bang

![The Big Bang](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as team
    participant P as production
    T->>T: 26 weeks of parallel work, no real traffic
    T->>P: cutover weekend, all four capabilities
    P-->>T: Monday: payment declines large orders
    T->>P: roll back, all four, because there is one switch
```

</details>

## 2. A Move By A Switch

![A Move By A Switch](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as team
    participant R as Router
    T->>R: pricing is SHADOW
    T->>R: differences are explained, pricing is NEW
    Note over T,R: stock, payment and email did not move
```

</details>

## 3. A One-Capability Rollback

![A One-Capability Rollback](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant R as Router
    participant P as new payment
    participant L as legacy
    R->>P: charge, large order
    P-->>R: declined
    Note over R: flip PAYMENT to LEGACY
    R->>L: charge
    L-->>R: charged
```

</details>

## 4. Two Sources Of Truth

![Two Sources Of Truth](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant R as Router
    participant N as new stock
    participant L as legacy stock table
    R->>N: reserve 5
    N-->>R: 395 on hand
    Note over L: still says 400, and its reports read it
```

</details>

