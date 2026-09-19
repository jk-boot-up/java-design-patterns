# Object Pool Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Connection Per Payment

![A Connection Per Payment](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as payment
    participant C as new connection
    P->>C: open, 200ms handshake
    P->>C: charge
    Note over P,C: thrown away, and again for the next payment
```

</details>

## 2. Borrow And Return

![Borrow And Return](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as payment
    participant Pool
    P->>Pool: borrow()
    Pool-->>P: an idle connection
    P->>Pool: giveBack()
    Note over Pool: 2 connections opened, ever
```

</details>

## 3. A Dirty Return

![A Dirty Return](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as Ada's payment
    participant Pool
    participant B as Grace's payment
    A->>Pool: giveBack(connection), no reset
    B->>Pool: borrow()
    Pool-->>B: the same connection
    B->>B: lastCardHolder() is Ada
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
    participant Pool
    participant P as third payment
    X->>Pool: borrow twice, never return
    P->>Pool: borrow(300ms)
    Pool-->>P: nothing, timed out
```

</details>

