# Unit of Work Pattern — UML Sequence Diagrams

Four sequences.

## 1. Objects Save Themselves

![Objects Save Themselves](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as placement
    participant DB as database
    P->>DB: insert order
    P->>DB: update stock 1, insert line 1
    P->>DB: update stock 2, insert line 2
    P->>DB: update stock 3, rejected
    Note over DB: half an order is left
```

</details>

## 2. A Transaction Around It

![A Transaction Around It](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as placement
    participant DB as database
    P->>DB: begin, locks held
    Note over P,DB: slow checks happen here, lock still held
    P->>DB: writes
    DB-->>P: rejected, rollback
```

</details>

## 3. The Unit Of Work Commits

![The Unit Of Work Commits](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as placement
    participant U as UnitOfWork
    participant DB as database
    P->>U: register seven changes
    P->>U: commit()
    U->>DB: begin
    U->>DB: seven writes, parents first
    U->>DB: commit
```

</details>

## 4. A Failed Commit

![A Failed Commit](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant U as UnitOfWork
    participant DB as database
    U->>DB: begin
    U->>DB: writes 1 to 6 succeed
    U->>DB: write 7 rejected
    U->>DB: rollback
    Note over DB: exactly as before
```

</details>

