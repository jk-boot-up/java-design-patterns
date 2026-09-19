# Object Pool with HikariCP Pattern — UML Sequence Diagrams

Four sequences.

## 1. Borrow And Return

![Borrow And Return](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as payment
    participant H as HikariCP
    P->>H: getConnection()
    H-->>P: opens one, demand needs it
    P->>H: close(), returned
    P->>H: getConnection()
    H-->>P: the same connection
```

</details>

## 2. A Reset On Return

![A Reset On Return](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as Ada's borrower
    participant H as HikariCP
    participant G as Grace's borrower
    A->>H: setAutoCommit(false), setReadOnly(true), close
    H->>H: reset both on return
    G->>H: getConnection()
    H-->>G: autoCommit true, readOnly false
```

</details>

## 3. A Leak Through The Session

![A Leak Through The Session](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as Ada's borrower
    participant DB as H2 session
    participant G as Grace's borrower
    A->>DB: set @card_holder = Ada Lovelace
    A->>A: close, returned
    G->>DB: select @card_holder
    DB-->>G: Ada Lovelace
```

</details>

## 4. An Exhausted Pool

![An Exhausted Pool](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant X as leaky borrowers
    participant H as HikariCP
    participant P as third caller
    X->>H: two connections, never returned
    P->>H: getConnection()
    H-->>P: SQLTransientConnectionException after connectionTimeout
```

</details>

