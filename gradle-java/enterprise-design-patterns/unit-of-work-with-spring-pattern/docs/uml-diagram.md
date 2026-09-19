# Unit of Work with Spring Pattern — UML Sequence Diagrams

Four sequences.

## 1. Writes Appear At Commit

![Writes Appear At Commit](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant B as the bean
    participant EM as persistence context
    participant DB as H2
    B->>EM: persist order, persist line, change stock
    Note over EM,DB: nothing written yet
    B-->>EM: method returns
    EM->>DB: 2 INSERTs, 1 UPDATE, then commit
```

</details>

## 2. An Unchecked Exception

![An Unchecked Exception](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as proxy
    participant B as the bean
    participant DB as H2
    P->>B: place()
    B-->>P: throws StockFailure
    P->>DB: rollback
    Note over DB: nothing was written
```

</details>

## 3. A Checked Exception

![A Checked Exception](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as proxy
    participant B as the bean
    participant DB as H2
    P->>B: place()
    B-->>P: throws StockFailureChecked
    P->>DB: commit, by default
    Note over DB: half an order
```

</details>

## 4. A Call On This

![A Call On This](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Caller
    participant P as proxy
    participant B as the bean
    Caller->>P: placeViaThis()
    P->>B: placeViaThis()
    B->>B: this.placeLines()
    Note over B: skips the proxy, no transaction
    B-->>Caller: TransactionRequiredException
```

</details>

